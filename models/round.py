import json
import os
from datetime import datetime

class Round:
    FILE_PATH = "data/rounds.json"

    def __init__(self, name, matches=None, start_date=None, end_date=None):
        self.name = name
        self.matches = matches if matches else []
        self.start_date = start_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_date = end_date

    def to_dict(self):
        """Convert Round object to dictionary."""
        return {
            "name": self.name,
            "matches": self.matches,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    def save(self):
        """Save the round to rounds.json."""
        rounds = []
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    rounds = json.load(f)
                except json.JSONDecodeError:
                    rounds = []
        rounds.append(self.to_dict())
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(rounds, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        """Load all rounds from rounds.json."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Round(**r) for r in data]
            except json.JSONDecodeError:
                return []
