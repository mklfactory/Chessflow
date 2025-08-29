import json
import os
import uuid

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, match_ids=None, start_date=None, end_date=None, round_id=None):
        self.id = round_id or str(uuid.uuid4())
        self.name = name
        self.match_ids = match_ids or []  # list of match UUIDs
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    def save(self):
        """Save or update the round in rounds.json"""
        rounds = []
        if os.path.exists(ROUNDS_FILE):
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                rounds = json.load(f)

        # update if exists
        for i, r in enumerate(rounds):
            if r["id"] == self.id:
                rounds[i] = self.to_dict()
                break
        else:
            rounds.append(self.to_dict())

        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump(rounds, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        if os.path.exists(ROUNDS_FILE):
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                return [Round(**r) for r in json.load(f)]
        return []

    @staticmethod
    def get_by_id(round_id):
        rounds = Round.load_all()
        for r in rounds:
            if r.id == round_id:
                return r
        return None
