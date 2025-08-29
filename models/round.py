import json
import uuid
from datetime import datetime
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, match_ids=None, start_time=None, end_time=None, round_id=None):
        self.id = round_id or str(uuid.uuid4())
        self.name = name
        self.match_ids = match_ids or []
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            match_ids=data.get("match_ids", []),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            round_id=data.get("id")
        )

    def save(self):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]
        rounds.append(self)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        try:
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Round.from_dict(d) for d in data]
        except FileNotFoundError:
            return []

    @staticmethod
    def load_by_id(round_id):
        for r in Round.load_all():
            if r.id == round_id:
                return r
        return None

    @staticmethod
    def start_round(round_obj):
        round_obj.start_time = datetime.now().isoformat()
        round_obj.save()

    def end_round(self):
        self.end_time = datetime.now().isoformat()
        self.save()

    def get_matches(self):
        return [Match.load_by_id(mid) for mid in self.match_ids]
