import json
import uuid
from pathlib import Path
from models.match import Match

DATA_FILE = Path("data/rounds.json")

class Round:
    def __init__(self, id=None, name="", matches=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.matches = matches or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "matches": self.matches,
        }

    def save(self):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]
        rounds.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=2)

    @classmethod
    def load_all(cls):
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE) as f:
            data = json.load(f)
        return [cls(**r) for r in data]

    @classmethod
    def load_by_id(cls, round_id):
        rounds = cls.load_all()
        for r in rounds:
            if r.id == round_id:
                return r
        return None

    @classmethod
    def delete(cls, round_id):
        rounds = cls.load_all()
        rounds = [r for r in rounds if r.id != round_id]
        with open(DATA_FILE, "w") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=2)

    @staticmethod
    def create_for_tournament(tournament):
        name = f"Round {len(tournament.rounds) + 1}"
        matches = Match.create_pairings(tournament.players)
        return Round(name=name, matches=matches)
