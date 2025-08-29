import json
import os
from datetime import datetime

class Round:
    def __init__(self, name, matches=None, start_time=None, end_time=None):
        self.name = name
        self.matches = matches or []  # list of dicts {"player1":..., "player2":..., "result":...}
        self.start_time = start_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = end_time

    def to_dict(self):
        return {
            "name": self.name,
            "matches": self.matches,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def save(self):
        """Save this round in rounds.json"""
        filename = "data/rounds.json"
        rounds = []

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    rounds = json.load(f)
                except json.JSONDecodeError:
                    rounds = []

        rounds.append(self.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(rounds, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        """Load all rounds from rounds.json"""
        filename = "data/rounds.json"
        if not os.path.exists(filename):
            return []

        with open(filename, "r", encoding="utf-8") as f:
            try:
                rounds_data = json.load(f)
            except json.JSONDecodeError:
                return []

        return [cls(**round_dict) for round_dict in rounds_data]
