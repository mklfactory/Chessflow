import json
import os
from datetime import datetime

class Round:
    FILE_PATH = "data/rounds.json"

    def __init__(self, name, matches=None, start_time=None, end_time=None):
        self.name = name
        self.matches = matches or []
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
        """Save this round to rounds.json"""
        rounds = Round.load_all()
        rounds.append(self)
        Round.save_all(rounds)

    @classmethod
    def save_all(cls, rounds):
        data = [r.to_dict() for r in rounds]
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        """Load all rounds from rounds.json"""
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [
                Round(
                    name=item["name"],
                    matches=item["matches"],
                    start_time=item["start_time"],
                    end_time=item.get("end_time"),
                )
                for item in data
            ]
