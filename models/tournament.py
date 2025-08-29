import json
import uuid
import os
from models.round import Round
from models.player import Player

TOURNAMENTS_FILE = "data/tournaments.json"
REPORT_FILE = "data/report.json"
os.makedirs("data", exist_ok=True)

class Tournament:
    def __init__(self, id=None, name="", location="", start_date="", end_date="", description="",
                 total_rounds=4, current_round=0, rounds=None, players=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.total_rounds = total_rounds
        self.current_round = current_round
        self.rounds = rounds or []
        self.players = players or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "total_rounds": self.total_rounds,
            "current_round": self.current_round,
            "rounds": [r.to_dict() for r in self.rounds],
            "players": [p.to_dict() for p in self.players],
        }

    @classmethod
    def from_dict(cls, data):
        rounds = [Round.from_dict(r) for r in data.get("rounds", [])]
        players = [Player.from_dict(p) for p in data.get("players", [])]
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            location=data.get("location", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            description=data.get("description", ""),
            total_rounds=data.get("total_rounds", 4),
            current_round=data.get("current_round", 0),
            rounds=rounds,
            players=players,
        )

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]
        tournaments.append(self)
        with open(TOURNAMENTS_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)

    @classmethod
    def load_all(cls):
        if not os.path.exists(TOURNAMENTS_FILE):
            return []
        with open(TOURNAMENTS_FILE) as f:
            data = json.load(f)
        return [cls.from_dict(t) for t in data]

    @classmethod
    def load_by_id(cls, tournament_id):
        for t in cls.load_all():
            if t.id == tournament_id:
                return t
        return None

    @classmethod
    def delete(cls, tournament_id):
        tournaments = cls.load_all()
        tournaments = [t for t in tournaments if t.id != tournament_id]
        with open(TOURNAMENTS_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)

    def add_player(self, player):
        if player.id not in [p.id for p in self.players]:
            self.players.append(player)

    def get_player_points(self):
        points = {p.id: 0 for p in self.players}
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if match.player1 and match.player1.id in points:
                    points[match.player1.id] += match.score1
                if match.player2 and match.player2.id in points:
                    points[match.player2.id] += match.score2
        return points

    def generate_report(self):
        report = {
            "tournament": self.to_dict(),
            "rounds": [r.to_dict() for r in self.rounds],
            "players": [p.to_dict() for p in self.players],
        }
        with open(REPORT_FILE, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[INFO] Rapport généré : {REPORT_FILE}")
