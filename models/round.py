import uuid
import json
import os
from models.match import Match

DATA_DIR = "data"
ROUNDS_FILE = os.path.join(DATA_DIR, "rounds.json")


class Round:
    def __init__(self, name, start_time, end_time=None, id=None, match_ids=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.match_ids = match_ids or []

    # ---------------------------
    # Relations
    # ---------------------------

    def add_match(self, match):
        """Add a match to this round (store only its ID)."""
        if match.id not in self.match_ids:
            self.match_ids.append(match.id)
            self.save()

    def get_matches(self):
        """Return list of Match objects for this round."""
        return [Match.load_by_id(mid) for mid in self.match_ids if Match.load_by_id(mid)]

    # ---------------------------
    # Persistence
    # ---------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "match_ids": self.match_ids,
        }

    def save(self):
        rounds = Round.load_all()
        rounds_dict = {r.id: r for r in rounds}
        rounds_dict[self.id] = self
        Round.save_all(list(rounds_dict.values()))

    @staticmethod
    def save_all(rounds):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4)

    @staticmethod
    def load_all():
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Round(**r) for r in data]

    @staticmethod
    def load_by_id(round_id):
        rounds = Round.load_all()
        for r in rounds:
            if r.id == round_id:
                return r
        return None

    @staticmethod
    def delete_by_id(round_id):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != round_id]
        Round.save_all(rounds)
