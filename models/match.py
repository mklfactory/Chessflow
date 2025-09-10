import uuid
import json
import os
from models.player import Player

DATA_DIR = "data"
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")
class Match:
    def __init__(self, player1_id, player2_id=None, score1=0.0, score2=0.0, id=None):
        self.id = id or str(uuid.uuid4())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def get_players(self):
        p1 = Player.load_by_id(self.player1_id)
        p2 = Player.load_by_id(self.player2_id) if self.player2_id else None
        return p1, p2

    def to_dict(self):
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "score1": self.score1,
            "score2": self.score2,
        }

    def save(self):
        matches = Match.load_all()
        matches = [m for m in matches if m.id != self.id]
        matches.append(self)
        Match.save_all(matches)

    @staticmethod
    def save_all(matches):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in matches], f, indent=4)

    @staticmethod
    def load_all():
        if not os.path.exists(MATCHES_FILE):
            return []
        with open(MATCHES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Match(**m) for m in data]

    @staticmethod
    def load_by_id(match_id):
        matches = Match.load_all()
        for m in matches:
            if m.id == match_id:
                return m
        return None

    @staticmethod
    def delete_by_id(match_id):
        matches = Match.load_all()
        matches = [m for m in matches if m.id != match_id]
        Match.save_all(matches)
