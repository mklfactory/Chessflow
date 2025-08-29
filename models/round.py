import json
import os
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, matches=None, start_time=None, end_time=None):
        self.name = name
        self.matches = matches if matches else []
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    def save(self, tournament_id):
        """Save round in rounds.json under its tournament_id"""
        if not os.path.exists("data"):
            os.makedirs("data")

        data = {}
        if os.path.exists(ROUNDS_FILE):
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        if str(tournament_id) not in data:
            data[str(tournament_id)] = []

        # Update or append round
        existing_rounds = data[str(tournament_id)]
        for i, r in enumerate(existing_rounds):
            if r["name"] == self.name:
                existing_rounds[i] = self.to_dict()
                break
        else:
            existing_rounds.append(self.to_dict())

        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_all(cls, tournament_id):
        """Load all rounds for a given tournament"""
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if str(tournament_id) not in data:
            return []

        rounds = []
        for r in data[str(tournament_id)]:
            matches = [Match.from_dict(m) for m in r["matches"]]
            rounds.append(
                cls(r["name"], matches, r.get("start_time"), r.get("end_time"))
            )
        return rounds
