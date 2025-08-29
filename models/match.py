import json
import os

MATCHES_FILE = "data/matches.json"

class Match:
    def __init__(self, player1_id, player2_id, score1=0.0, score2=0.0, match_id=None):
        self.id = match_id
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
        matches = Match.load_all()

        # assign new ID if necessary
        if not self.id:
            self.id = len(matches) + 1

        # update or append
        updated = False
        for i, m in enumerate(matches):
            if m["id"] == self.id:
                matches[i] = self.to_dict()
                updated = True
                break
        if not updated:
            matches.append(self.to_dict())

        with open(MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        if not os.path.exists(MATCHES_FILE):
            return []
        with open(MATCHES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def load_by_id(match_id):
        matches = Match.load_all()
        for m in matches:
            if m["id"] == match_id:
                return Match(
                    player1_id=m["player1_id"],
                    player2_id=m["player2_id"],
                    score1=m.get("score1", 0.0),
                    score2=m.get("score2", 0.0),
                    match_id=m["id"]
                )
        return None
