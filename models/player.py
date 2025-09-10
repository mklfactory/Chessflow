import json
import uuid
import re

DATA_FILE = "data/players.json"
ID_PATTERN = re.compile(r"^[A-Za-z]{2}\d{5}$")
class Player:
    def __init__(self, id=None, first_name="", last_name="", birth_date="", gender="", national_id=""):
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.national_id = national_id

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "national_id": self.national_id,
        }

    @staticmethod
    def from_dict(data):
        return Player(
            id=data.get("id"),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            birth_date=data.get("birth_date", ""),
            gender=data.get("gender", ""),
            national_id=data.get("national_id", "")
        )

    def save(self):
        players = Player.load_all()
        players = [p for p in players if p.id != self.id]
        players.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    @staticmethod
    def load_all():
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            return [Player.from_dict(p) for p in data]
        except Exception:
            return []

    @staticmethod
    def load_by_id(player_id):
        players = Player.load_all()
        for p in players:
            if p.id == player_id:
                return p
        return None

    @staticmethod
    def delete(player_id):
        players = Player.load_all()
        players = [p for p in players if p.id != player_id]
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    def full_name(self):
        return f"{self.last_name} {self.first_name}".strip()

    @staticmethod
    def sort_alphabetically(players):
        return sorted(players, key=lambda p: (p.last_name.lower(), p.first_name.lower()))

    @staticmethod
    def is_valid_national_id(value: str) -> bool:
        return bool(ID_PATTERN.match(value or ""))
