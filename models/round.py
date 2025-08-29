import json
import os
from datetime import datetime
from models.match import Match

ROUNDS_FILE = "data/rounds.json"


class Round:
    def __init__(self, name, matches=None, start_time=None, end_time=None, tournament_id=None):
        self.name = name
        self.matches = matches if matches else []
        self.start_time = start_time if start_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = end_time
        self.tournament_id = tournament_id  # 🔹 Identifiant du tournoi parent

    def end_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "tournament_id": self.tournament_id,
        }

    @classmethod
    def from_dict(cls, data):
        matches = [Match.from_dict(m) for m in data.get("matches", [])]
        return cls(
            name=data["name"],
            matches=matches,
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            tournament_id=data.get("tournament_id")
        )

    def save(self):
        rounds = Round.load_all()
        rounds.append(self)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls, tournament_id=None):
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        rounds = [cls.from_dict(d) for d in data]
        if tournament_id:
            rounds = [r for r in rounds if r.tournament_id == tournament_id]
        return rounds

    @classmethod
    def save_all(cls, rounds):
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)
