import json
import uuid
from pathlib import Path

DATA_FILE = Path("data/tournaments.json")

class Tournament:
    def __init__(self, id=None, name="", location="", start_date="", end_date="", description="", players=None, rounds=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.players = players or []
        self.rounds = rounds or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "players": self.players,
            "rounds": [r.to_dict() for r in self.rounds]
        }

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]
        tournaments.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)

    @classmethod
    def load_all(cls):
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE) as f:
            data = json.load(f)
        return [cls(**t) for t in data]

    @classmethod
    def load_by_id(cls, tournament_id):
        tournaments = cls.load_all()
        for t in tournaments:
            if t.id == tournament_id:
                return t
        return None

    @classmethod
    def delete(cls, tournament_id):
        tournaments = cls.load_all()
        tournaments = [t for t in tournaments if t.id != tournament_id]
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)
