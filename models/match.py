# models/match.py
import json
import os

class Match:
    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "score1": self.score1,
            "score2": self.score2,
        }

    def save(self):
        """Save this match to matchs.json"""
        path = "data/matchs.json"
        if not os.path.exists("data"):
            os.makedirs("data")

        matchs = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    matchs = json.load(f)
                except json.JSONDecodeError:
                    matchs = []

        matchs.append(self.to_dict())

        with open(path, "w", encoding="utf-8") as f:
            json.dump(matchs, f, indent=4, ensure_ascii=False)
