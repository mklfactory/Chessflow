import json
import os
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, round_id=None, match_ids=None, start_time=None, end_time=None):
        self.id = round_id
        self.name = name
        self.match_ids = match_ids or []
        self.start_time = start_time
        self.end_time = end_time

    @property
    def matches(self):
        return [Match.load_by_id(mid) for mid in self.match_ids]

    def add_match(self, match):
        self.match_ids.append(match.id)
        match.save()
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def save(self):
        rounds = Round.load_all()
        # assign new ID if necessary
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

    @staticmethod
    def load_by_id(round_id):
        rounds = Round.load_all()
        for r in rounds:
            if r["id"] == round_id:
                return Round(
                    name=r["name"],
                    round_id=r["id"],
                    match_ids=r.get("match_ids", []),
                    start_time=r.get("start_time"),
                    end_time=r.get("end_time")
                )
        return None
