import json
import os
from models.round import Round
from models.player import Player

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
        t = Tournament(
            data["name"], data["place"], data["start_date"],
            data["end_date"], data["description"], data.get("rounds", 4)
        )
        t.current_round = data.get("current_round", 0)
        t.players = [Player.from_dict(p) for p in data["players"]]
        t.round_list = [Round(r["name"]) for r in data.get("round_list", [])]
        return t

    def save(self, filepath="data/tournaments.json"):
        tournaments = Tournament.load_all(filepath)
        tournaments.append(self)
        Tournament.save_all(tournaments, filepath)

    @staticmethod
    def load_all(filepath="data/tournaments.json"):
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return [Tournament.from_dict(t) for t in json.load(f)]

    @staticmethod
    def save_all(tournaments, filepath="data/tournaments.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=4)
