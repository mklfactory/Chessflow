# models/tournament.py
import json
import os
import uuid
from pathlib import Path
from datetime import datetime

from .round import Round  # use Round.load_all to fetch rounds by tournament_id

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "tournaments.json"
REPORTS_PATH = DATA_DIR / "reports.json"


class Tournament:
    """Tournament model persisted to data/tournaments.json (list of dicts).
    Fields are permissive for backward compatibility.
    """

    def __init__(
        self,
        id=None,
        name="",
        location="",
        start_date=None,
        end_date=None,
        number_of_rounds=4,
        current_round=0,
        players=None,
        rounds=None,
        description="",
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date or datetime.now().strftime("%Y-%m-%d")
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        # players: could be list of player dicts or player ids; we keep as-is
        self.players = players if players is not None else []
        # rounds: we do not store full round objects here; store list of round ids or names
        self.rounds = rounds if rounds is not None else []
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "rounds": self.rounds,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        # Accept different key names for compatibility
        id_ = data.get("id") or data.get("tournament_id") or data.get("name")
        name = data.get("name") or data.get("tournament_name") or ""
        location = data.get("location") or data.get("place") or ""
        start_date = data.get("start_date") or data.get("date") or None
        end_date = data.get("end_date") or data.get("end") or None
        number_of_rounds = data.get("number_of_rounds") or data.get("total_rounds") or 4
        current_round = data.get("current_round") or 0
        players = data.get("players", [])
        rounds = data.get("rounds", [])
        description = data.get("description", "") or data.get("notes", "")
        return cls(
            id=id_,
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            current_round=current_round,
            players=players,
            rounds=rounds,
            description=description,
        )

    # ---------- Persistence helpers ----------

    @staticmethod
    def _ensure_data_dir():
        if not DATA_DIR.exists():
            print(f"[DEBUG] Creating data directory: {DATA_DIR}")
            DATA_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _read_raw_file(cls):
        cls._ensure_data_dir()
        if not FILE_PATH.exists():
            print(f"[DEBUG] tournaments file not found: {FILE_PATH}")
            return None
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"[DEBUG] Loaded tournaments raw data from {FILE_PATH}")
            return data
        except json.JSONDecodeError:
            print(f"[DEBUG] tournaments file {FILE_PATH} is empty or invalid JSON")
            return None

    @classmethod
    def _normalize_raw(cls, raw):
        """Normalize raw tournaments JSON into a list of tournament dicts."""
        if raw is None:
            return []

        if isinstance(raw, list):
            return raw

        if isinstance(raw, dict):
            # Two possible historic formats:
            # 1) dict mapping id -> tournament_dict
            # 2) dict list-like (mapping keys arbitrary) -> convert to list(values)
            values = list(raw.values())
            # If values are dicts and contain id/name, use them
            if all(isinstance(v, dict) for v in values):
                return values
            # fallback
            return values

        print(f"[DEBUG] Unknown tournaments JSON format: {type(raw)}")
        return []

    @classmethod
    def load_all(cls):
        """Return list of Tournament instances (backward compatible)."""
        raw = cls._read_raw_file()
        normalized = cls._normalize_raw(raw)
        tournaments = [cls.from_dict(item) for item in normalized]
        print(f"[DEBUG] load_all returned {len(tournaments)} tournaments")
        return tournaments

    def save(self):
        """Save or update this tournament in tournaments.json (list format)."""
        raw = self._read_raw_file()
        normalized = self._normalize_raw(raw)

        updated = False
        for i, item in enumerate(normalized):
            existing_id = item.get("id") or item.get("tournament_id") or item.get("name")
            if str(existing_id) == str(self.id):
                normalized[i] = self.to_dict()
                updated = True
                break

        if not updated:
            normalized.append(self.to_dict())

        self._ensure_data_dir()
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=4, ensure_ascii=False)
        print(f"[DEBUG] Tournament.save(): {'updated' if updated else 'added'} tournament id={self.id} name={self.name}")

    @classmethod
    def save_all(cls, tournaments):
        """Overwrite file with a list of tournament dicts."""
        cls._ensure_data_dir()
        data = [t.to_dict() if isinstance(t, Tournament) else t for t in tournaments]
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[DEBUG] Saved {len(data)} tournaments to {FILE_PATH}")

    @classmethod
    def get_by_id(cls, tournament_id):
        for t in cls.load_all():
            if str(t.id) == str(tournament_id):
                return t
        print(f"[DEBUG] Tournament.get_by_id: not found id={tournament_id}")
        return None

    # ---------- Reports ----------

    def generate_report(self):
        """Generate a JSON report containing tournament data and its related rounds."""
        rounds = Round.load_all(tournament_id=self.id)
        report = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "rounds": [r.to_dict() for r in rounds],
            "description": self.description,
            "generated_at": datetime.now().isoformat(),
        }

        self._ensure_data_dir()
        # Load existing reports (list), update or append
        reports = []
        if REPORTS_PATH.exists():
            try:
                with open(REPORTS_PATH, "r", encoding="utf-8") as f:
                    reports = json.load(f)
            except json.JSONDecodeError:
                reports = []

        # replace report for this tournament if exists
        replaced = False
        for i, r in enumerate(reports):
            if str(r.get("id")) == str(self.id):
                reports[i] = report
                replaced = True
                break
        if not replaced:
            reports.append(report)

        with open(REPORTS_PATH, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=4, ensure_ascii=False)
        print(f"[DEBUG] generate_report: saved report for tournament id={self.id} to {REPORTS_PATH}")
        return report
