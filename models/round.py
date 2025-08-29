import json
import os

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, matches_ids=None, round_id=None):
        self.id = round_id
        self.name = name
        self.matches_ids = matches_ids or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "matches_ids": self.matches_ids,
        }

    def save(self):
        rounds = []
        if os.path.exists(ROUNDS_FILE):
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                try:
                    rounds = json.load(f)
                except json.JSONDecodeError:
                    rounds = []

        # assign ID if new
        if not self.id:
            self.id = len(rounds) + 1

        # update or append
        updated = False
        for i, r in enumerate(rounds):
            if r["id"] == self.id:
                rounds[i] = self.to_dict()
                updated = True
                break
        if not updated:
            rounds.append(self.to_dict())

        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump(rounds, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
