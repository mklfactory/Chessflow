import uuid
from datetime import datetime

class Round:
    def __init__(self, id=None, name="", matches=None, start_time=None, end_time=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.matches = matches or []  # liste d’objets Match
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "matches": [m.to_list() for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @staticmethod
    def from_dict(data):
        from models.match import Match
        matches = [Match.from_list(m) for m in data.get("matches", [])]
        return Round(
            id=data.get("id"),
            name=data.get("name"),
            matches=matches,
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )

    @staticmethod
    def start_round(round_obj):
        round_obj.start_time = datetime.now().isoformat()

    @staticmethod
    def end_round(round_obj):
        round_obj.end_time = datetime.now().isoformat()
