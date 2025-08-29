# models/round.py
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

# Simple debug prints are included to help trace file I/O and flow.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "rounds.json"


class Round:
    """Round model saved in data/rounds.json.
    Each round dict contains at least:
      - id (unique id)
      - tournament_id (to link to tournament)
      - name
      - matches (list of match dicts)
      - start_time, end_time (ISO strings or None)
    """

    def __init__(self, id=None, tournament_id=None, name="", matches=None, start_time=None, end_time=None):
        self.id = id or str(uuid.uuid4())
        self.tournament_id = tournament_id
        self.name = name
        # matches expected to be list of dicts (flexible for different match representations)
        self.matches = matches if matches is not None else []
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "name": self.name,
            "matches": self.matches,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data):
        # data may come from older formats; stay permissive
        return cls(
            id=data.get("id") or data.get("round_id"),
            tournament_id=data.get("tournament_id") or data.get("tournament"),
            name=data.get("name") or data.get("round_name") or "",
            matches=data.get("matches", []),
            start_time=data.get("start_time") or data.get("start_date"),
            end_time=data.get("end_time") or data.get("end_date"),
        )

    # ---------- Persistence helpers ----------

    @staticmethod
    def _ensure_data_dir():
        if not DATA_DIR.exists():
            print(f"[DEBUG] Creating data directory: {DATA_DIR}")
            DATA_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _read_raw_file(cls):
        """Read the file and return python object. Handle missing or invalid file gracefully."""
        cls._ensure_data_dir()
        if not FILE_PATH.exists():
            print(f"[DEBUG] rounds file not found: {FILE_PATH}")
            return None
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"[DEBUG] Loaded rounds raw data from {FILE_PATH}")
            return data
        except json.JSONDecodeError:
            print(f"[DEBUG] rounds file {FILE_PATH} is empty or invalid JSON")
            return None

    @classmethod
    def _normalize_raw(cls, raw):
        """Normalize raw content into a list of round dicts.
        Accept either:
          - a dict mapping tournament_id -> [rounds...]
          - a list of round dicts
        Return list of round dicts (each including tournament_id).
        """
        if raw is None:
            return []

        if isinstance(raw, list):
            # Already list of rounds
            return raw

        if isinstance(raw, dict):
            # Could be {tournament_id: [rounds], ...} or {id: round_dict, ...}
            rounds = []
            # detect if values are lists -> mapping by tournament
            any_list_values = any(isinstance(v, list) for v in raw.values())
            if any_list_values:
                for t_id, r_list in raw.items():
                    for r in r_list:
                        if isinstance(r, dict):
                            # ensure tournament_id present
                            r.setdefault("tournament_id", t_id)
                            rounds.append(r)
            else:
                # maybe dict of id -> round_dict
                for _id, r in raw.items():
                    if isinstance(r, dict):
                        r.setdefault("id", _id)
                        rounds.append(r)
            return rounds

        # unknown format
        print(f"[DEBUG] Unknown rounds JSON format: {type(raw)}")
        return []

    @classmethod
    def load_all(cls, tournament_id=None):
        """Return list of Round instances. If tournament_id provided, filter for that tournament."""
        raw = cls._read_raw_file()
        normalized = cls._normalize_raw(raw)
        rounds = [cls.from_dict(r) for r in normalized]

        if tournament_id is not None:
            rounds = [r for r in rounds if str(r.tournament_id) == str(tournament_id)]

        print(f"[DEBUG] load_all returned {len(rounds)} rounds (filter tournament_id={tournament_id})")
        return rounds

    @classmethod
    def save_all(cls, rounds):
        """Save a list of Round instances (overwrites file). We store as a list of dicts."""
        cls._ensure_data_dir()
        data = [r.to_dict() if isinstance(r, Round) else r for r in rounds]
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[DEBUG] Saved {len(data)} rounds to {FILE_PATH}")

    def save(self):
        """Save or update this round in rounds.json (list-of-dicts format)."""
        raw = self._read_raw_file()
        normalized = self._normalize_raw(raw)
        # find by id, update, else append
        updated = False
        for i, r in enumerate(normalized):
            if str(r.get("id")) == str(self.id):
                normalized[i] = self.to_dict()
                updated = True
                break
        if not updated:
            normalized.append(self.to_dict())

        self._ensure_data_dir()
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=4, ensure_ascii=False)
        print(f"[DEBUG] Round.save(): {'updated' if updated else 'added'} round id={self.id} name={self.name}")
