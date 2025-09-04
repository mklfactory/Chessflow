import json
import os
from datetime import datetime
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    def __init__(self, name, round_id=None, match_ids=None, start_time=None, end_time=None):
        self.id = round_id
        self.name = name
        self.match_ids = match_ids or []  # liste des IDs de matchs
        self.start_time = start_time
        self.end_time = end_time

    # ---------------------------
    # Gestion des matchs
    # ---------------------------

    @property
    def matches(self):
        # retourne les objets Match correspondants aux match_ids
        all_matches = Match.load_all()
        return [m for m in all_matches if m.id in self.match_ids]

    def add_match(self, match):
        if match.id not in self.match_ids:
            self.match_ids.append(match.id)
            match.save()
            self.save()

    # ---------------------------
    # Conversion dict <-> objet
    # ---------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            round_id=data.get("id"),
            match_ids=data.get("match_ids", []),
            start_time=data.get("start_time"),
            end_time=data.get("end_time")
        )

    # ---------------------------
    # Sauvegarde / chargement
    # ---------------------------

    def save(self):
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]

        # assigner un nouvel ID si nécessaire
        if not self.id:
            self.id = str(len(rounds) + 1)

        rounds.append(self)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Round.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    @staticmethod
    def load_by_id(round_id):
        for r in Round.load_all():
            if r.id == round_id:
                return r
        return None

    # ---------------------------
    # Début / fin du round
    # ---------------------------

    def start_round(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def end_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()
