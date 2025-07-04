from datetime import datetime
from models.match import Match
import random

class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None

    def generate_matches(self, players):
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        random.shuffle(sorted_players)
        for i in range(0, len(sorted_players), 2):
            if i + 1 < len(sorted_players):
                match = Match(sorted_players[i], sorted_players[i+1])
                self.matches.append(match)

    def end_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_tuple() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
