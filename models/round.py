# models/round.py
import json
import os

class Round:
    def __init__(self, name, matches=None):
        self.name = name
        self.matches = matches if matches else []

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
        }

    def save(self):
        """Save this round to rounds.json (without matchs inside)"""
        path = "data/rounds.json"
        if not os.path.exists("data"):
            os.makedirs("data")

        rounds = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    rounds = json.load(f)
                except json.JSONDecodeError:
                    rounds = []

        rounds.append({
            "name": self.name
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(rounds, f, indent=4, ensure_ascii=False)

        # Save each match separately in matchs.json
        for match in self.matches:
            match.save()
