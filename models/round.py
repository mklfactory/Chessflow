import json
import uuid
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name="", match_ids=None, round_id=None):
        self.id = round_id or str(uuid.uuid4())
        self.name = name
        self.match_ids = match_ids or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            match_ids=data.get("match_ids", []),
            round_id=data.get("id")
        )

    def save(self):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]
        rounds.append(self)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_all():
        try:
            with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Round.from_dict(d) for d in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def load_by_id(round_id):
        for r in Round.load_all():
            if r.id == round_id:
                return r
        return None

    @staticmethod
    def start_round(round_obj):
        # Placeholder pour le début du round
        # On peut ajouter ici un timestamp ou autre
        pass

    def update_match_result(self, match_id, score1, score2):
        if match_id in self.match_ids:
            match = Match.load_by_id(match_id)
            if match:
                match.score1 = score1
                match.score2 = score2
                match.save()

    def get_matches(self):
        matches = []
        for m_id in self.match_ids:
            match = Match.load_by_id(m_id)
            if match:
                matches.append(match)
        return matches
