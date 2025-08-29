import json
import os
from datetime import datetime

class Tournament:
    def __init__(self, name, location, date=None, players=None, time_control="bullet", description="", rounds=None):
        self.name = name
        self.location = location
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.players = players or []
        self.time_control = time_control
        self.description = description
        self.rounds = rounds or []  # will store only references (names), not full round data

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "time_control": self.time_control,
            "description": self.description,
            "rounds": [r if isinstance(r, str) else r.name for r in self.rounds],
        }

    def save(self):
        """Save tournament in tournaments.json"""
        filename = "data/tournaments.json"
        tournaments = []

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    tournaments = json.load(f)
                except json.JSONDecodeError:
                    tournaments = []

        # Check if tournament already exists -> replace
        updated = False
        for i, t in enumerate(tournaments):
            if t["name"] == self.name:
                tournaments[i] = self.to_dict()
                updated = True
                break
        if not updated:
            tournaments.append(self.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tournaments, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        filename = "data/tournaments.json"
        if not os.path.exists(filename):
            return []

        with open(filename, "r", encoding="utf-8") as f:
            try:
                tournaments_data = json.load(f)
            except json.JSONDecodeError:
                return []

        return [cls(**tournament_dict) for tournament_dict in tournaments_data]

    def export_report(self):
        """Export a tournament report with players, rounds (references), etc."""
        report = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
            "rounds": [r if isinstance(r, str) else r.name for r in self.rounds],
            "time_control": self.time_control,
            "description": self.description,
        }

        filename = "data/report.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        return filename
