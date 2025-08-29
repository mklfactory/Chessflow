import json
import os

class Tournament:
    FILE_PATH = "data/tournaments.json"
    REPORT_PATH = "data/reports.json"

    def __init__(self, name, location, date, players=None, rounds=None):
        self.name = name
        self.location = location
        self.date = date
        self.players = players if players else []
        self.rounds = rounds if rounds else []

    def to_dict(self):
        """Convert Tournament object to dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "rounds": [r if isinstance(r, dict) else r.to_dict() for r in self.rounds],
        }

    def save(self):
        """Save tournament to tournaments.json."""
        tournaments = []
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    tournaments = json.load(f)
                except json.JSONDecodeError:
                    tournaments = []
        tournaments.append(self.to_dict())
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(tournaments, f, indent=4, ensure_ascii=False)

    def generate_report(self):
        """Generate and save a report for this tournament into reports.json."""
        report = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "rounds": [r if isinstance(r, dict) else r.to_dict() for r in self.rounds],
        }

        reports = []
        if os.path.exists(self.REPORT_PATH):
            with open(self.REPORT_PATH, "r", encoding="utf-8") as f:
                try:
                    reports = json.load(f)
                except json.JSONDecodeError:
                    reports = []

        reports.append(report)
        with open(self.REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        """Load all tournaments from tournaments.json."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Tournament(**t) for t in data]
            except json.JSONDecodeError:
                return []
