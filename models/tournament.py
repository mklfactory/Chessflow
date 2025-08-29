import json
import os
from models.round import Round

TOURNAMENTS_FILE = "data/tournaments.json"
REPORTS_FILE = "data/reports.json"

class Tournament:
    def __init__(self, tournament_id, name, location, date, players=None, rounds=None):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.date = date
        self.players = players if players else []
        self.rounds = rounds if rounds else []

    def to_dict(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "players": self.players,
        }

    def save(self):
        """Save tournament without rounds (stored separately)"""
        if not os.path.exists("data"):
            os.makedirs("data")

        data = {}
        if os.path.exists(TOURNAMENTS_FILE):
            with open(TOURNAMENTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data[str(self.tournament_id)] = self.to_dict()

        with open(TOURNAMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_all(cls):
        if not os.path.exists(TOURNAMENTS_FILE):
            return []
        with open(TOURNAMENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        tournaments = []
        for t_id, t_data in data.items():
            tournaments.append(
                cls(
                    tournament_id=t_data["tournament_id"],
                    name=t_data["name"],
                    location=t_data["location"],
                    date=t_data["date"],
                    players=t_data.get("players", []),
                    rounds=Round.load_all(t_data["tournament_id"])
                )
            )
        return tournaments

    def generate_report(self):
        """Generate tournament report (players, rounds, matches) in JSON"""
        report = {
            "tournament": self.to_dict(),
            "rounds": [r.to_dict() for r in Round.load_all(self.tournament_id)]
        }

        if not os.path.exists("data"):
            os.makedirs("data")

        data = {}
        if os.path.exists(REPORTS_FILE):
            with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data[str(self.tournament_id)] = report

        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return report
