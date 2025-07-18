import json
import uuid
from pathlib import Path

DATA_FILE = Path("data/players.json")

class Player:
    def __init__(self, id=None, first_name="", last_name="", birthdate="", ranking=0):
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.ranking = ranking

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
            "ranking": self.ranking
        }

    def save(self):
        players = Player.load_all()
        players = [p for p in players if p.id != self.id]
        players.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    @classmethod
    def load_all(cls):
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE) as f:
            data = json.load(f)
        return [cls(**player) for player in data]

    @classmethod
    def load_by_id(cls, player_id):
        players = cls.load_all()
        for player in players:
            if player.id == player_id:
                return player
        return None

    @classmethod
    def delete(cls, player_id):
        players = cls.load_all()
        players = [p for p in players if p.id != player_id]
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)
