import json
import os
import uuid

MATCHES_FILE = "data/matches.json"

class Match:
    def __init__(self, player1_id, player2_id, score1=0.0, score2=0.0, match_id=None):
        self.id = match_id or str(uuid.uuid4())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "score1": self.score1,
            "score2": self.score2,
        }

    def save(self):
        """Save or update the match in matches.json"""
        matches = []
        if os.path.exists(MATCHES_FILE):
            with open(MATCHES_FILE, "r", encoding="utf-8") as f:
                matches = json.load(f)

        # update if exists
        for i, m in enumerate(matches):
            if m["id"] == self.id:
                matches[i] = self.to_dict()
                break
        else:
            matches.append(self.to_dict())

        with open(MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        if os.path.exists(MATCHES_FILE):
            with open(MATCHES_FILE, "r", encoding="utf-8") as f:
                return [Match(**m) for m in json.load(f)]
        return []

    @staticmethod
    def get_by_id(match_id):
        matches = Match.load_all()
        for m in matches:
            if m.id == match_id:
                return m
        return None
