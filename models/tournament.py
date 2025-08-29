import json
import os
from datetime import datetime
from .round import Round

class Tournament:
    FILE_PATH = "data/tournaments.json"
    REPORT_PATH = "data/reports.json"

    def __init__(self, name, location, date=None, players=None, rounds=None):
        self.name = name
        self.location = location
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.players = players or []
        self.rounds = rounds or []  # list of round names (references)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "rounds": self.rounds,  # only references to Round names
        }

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.name != self.name]
        tournaments.append(self)
        Tournament.save_all(tournaments)

    @classmethod
    def save_all(cls, tournaments):
        data = [t.to_dict() for t in tournaments]
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [
                Tournament(
                    name=item["name"],
                    location=item["location"],
                    date=item["date"],
                    players=item.get("players", []),
                    rounds=item.get("rounds", []),
                )
                for item in data
            ]

    # -------- Reports ----------
    def generate_report(self):
        """Generate a JSON report for this tournament"""
        report = {
            "tournament": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "rounds": [],
        }

        all_rounds = Round.load_all()
        for round_name in self.rounds:
            r = next((x for x in all_rounds if x.name == round_name), None)
            if r:
                report["rounds"].append(r.to_dict())

        # Save into reports.json
        os.makedirs(os.path.dirname(self.REPORT_PATH), exist_ok=True)
        if os.path.exists(self.REPORT_PATH):
            with open(self.REPORT_PATH, "r", encoding="utf-8") as f:
                reports = json.load(f)
        else:
            reports = []

        reports = [rep for rep in reports if rep["tournament"] != self.name]
        reports.append(report)

        with open(self.REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=4, ensure_ascii=False)

        return report
