import json
import os
from models.player import Player
from models.round import Round

TOURNAMENTS_FILE = "data/tournaments.json"
REPORTS_FILE = "data/reports.json"


class Tournament:
    def __init__(self, name, location, date, number_of_rounds=4, players=None, id=None):
        self.id = id if id else name.replace(" ", "_").lower()
        self.name = name
        self.location = location
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.players = players if players else []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "number_of_rounds": self.number_of_rounds,
            "players": [p.to_dict() for p in self.players],
        }

    @classmethod
    def from_dict(cls, data):
        players = [Player.from_dict(p) for p in data.get("players", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            date=data["date"],
            number_of_rounds=data.get("number_of_rounds", 4),
            players=players
        )

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]  # supprime doublons
        tournaments.append(self)
        with open(TOURNAMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        if not os.path.exists(TOURNAMENTS_FILE):
            return []
        with open(TOURNAMENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [cls.from_dict(d) for d in data]

    @classmethod
    def get_by_id(cls, tournament_id):
        tournaments = cls.load_all()
        for t in tournaments:
            if t.id == tournament_id:
                return t
        return None

    def generate_report(self):
        """ Génère un rapport complet du tournoi avec rounds et résultats """
        rounds = Round.load_all(tournament_id=self.id)
        report = {
            "tournament": self.to_dict(),
            "rounds": [r.to_dict() for r in rounds],
        }

        # Sauvegarde dans reports.json
        if os.path.exists(REPORTS_FILE):
            with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data = [r for r in data if r["tournament"]["id"] != self.id]  # supprime anciens rapports
        data.append(report)

        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return report
