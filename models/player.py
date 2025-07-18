import json
import os

class Player:
    def __init__(self, national_id, last_name, first_name, birth_date):
        self.national_id = national_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.score = 0

    def to_dict(self):
        return {
            "national_id": self.national_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "score": self.score,
        }

    @staticmethod
    def from_dict(data):
        player = Player(
            data["national_id"],
            data["last_name"],
            data["first_name"],
            data["birth_date"]
        )
        player.score = data.get("score", 0)
        return player

    def save(self, filepath="data/players.json"):
        players = Player.load_all(filepath)
        players.append(self)
        Player.save_all(players, filepath)

    @staticmethod
    def load_all(filepath="data/players.json"):
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return [Player.from_dict(p) for p in json.load(f)]

    @staticmethod
    def save_all(players, filepath="data/players.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in players], f, indent=4)
