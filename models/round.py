import json
import uuid
from datetime import datetime
from models.match import Match

ROUND_FILE = "data/rounds.json"

class Round:
    def __init__(self, id=None, name="", matches=None, start_time=None, end_time=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.matches = matches or []
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "matches": [m.to_list() for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @staticmethod
    def from_dict(data):
        matches = [Match.from_list(m) for m in data.get("matches", [])]
        return Round(
            id=data.get("id"),
            name=data.get("name", ""),
            matches=matches,
            start_time=data.get("start_time"),
            end_time=data.get("end_time")
        )

    def save(self):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]
        rounds.append(self)
        with open(ROUND_FILE, "w") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=2)

    @staticmethod
    def load_all():
        try:
            with open(ROUND_FILE) as f:
                data = json.load(f)
            return [Round.from_dict(r) for r in data]
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

    @staticmethod
    def end_round(round_obj):
        round_obj.end_time = datetime.now().isoformat()
        round_obj.save()
