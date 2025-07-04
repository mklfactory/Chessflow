from models.player import Player
from models.round import Round

class Tournament:
    def __init__(self, name, place, start_date, end_date, description, rounds=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.rounds = rounds
        self.current_round = 0
        self.round_list = []
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_obj):
        self.round_list.append(round_obj)
        self.current_round += 1

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "rounds": self.rounds,
            "current_round": self.current_round,
            "players": [p.to_dict() for p in self.players],
            "round_list": [r.to_dict() for r in self.round_list]
        }

    @staticmethod
    def from_dict(data):
        tournament = Tournament(
            data["name"],
            data["place"],
            data["start_date"],
            data["end_date"],
            data["description"],
            data["rounds"]
        )
        tournament.current_round = data["current_round"]
        tournament.players = [Player.from_dict(p) for p in data["players"]]
        return tournament
