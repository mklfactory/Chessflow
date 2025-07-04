from models.round import Round
from models.player import Player


class Tournament:
    def __init__(self, name, place, start_date, end_date, description="", number_of_rounds=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.rounds = []
        self.players = []

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [r.to_dict() for r in self.rounds],
            "players": [p.to_dict() for p in self.players]
        }

    @staticmethod
    def from_dict(data):
        t = Tournament(
            data["name"],
            data["place"],
            data["start_date"],
            data["end_date"],
            data.get("description", ""),
            data.get("number_of_rounds", 4)
        )
        t.current_round = data.get("current_round", 0)
        t.players = [Player.from_dict(p) for p in data.get("players", [])]
        t.rounds = [Round.from_dict(r) for r in data.get("rounds", [])]
        return t

    def __str__(self):
        return f"{self.name} - {self.place} ({self.start_date} au {self.end_date})"
