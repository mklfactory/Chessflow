import uuid
import json
import os
from models.round import Round
from models.player import Player

DATA_DIR = "data"
TOURNAMENTS_FILE = os.path.join(DATA_DIR, "tournaments.json")


class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        description,
        total_rounds=4,
        id=None,
        player_ids=None,
        round_ids=None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.total_rounds = total_rounds
        self.player_ids = player_ids or []
        self.round_ids = round_ids or []

    # ---------------------------
    # Relations
    # ---------------------------

    def add_player(self, player):
        """Add a player to this tournament (store only its ID)."""
        if player.id not in self.player_ids:
            self.player_ids.append(player.id)
            self.save()

    def get_players(self):
        """Return list of Player objects for this tournament."""
        return [Player.load_by_id(pid) for pid in self.player_ids if Player.load_by_id(pid)]

    def add_round(self, round_obj):
        """Add a round to this tournament (store only its ID)."""
        if round_obj.id not in self.round_ids:
            self.round_ids.append(round_obj.id)
            self.save()

    def get_rounds(self):
        """Return list of Round objects for this tournament."""
        return [Round.load_by_id(rid) for rid in self.round_ids if Round.load_by_id(rid)]

    # ---------------------------
    # Persistence
    # ---------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "total_rounds": self.total_rounds,
            "player_ids": self.player_ids,
            "round_ids": self.round_ids,
        }

    def save(self):
        tournaments = Tournament.load_all()
        tournaments_dict = {t.id: t for t in tournaments}
        tournaments_dict[self.id] = self
        Tournament.save_all(list(tournaments_dict.values()))

    @staticmethod
    def save_all(tournaments):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(TOURNAMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=4)

    @staticmethod
    def load_all():
        if not os.path.exists(TOURNAMENTS_FILE):
            return []
        with open(TOURNAMENTS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Tournament(**t) for t in data]

    @staticmethod
    def load_by_id(tournament_id):
        tournaments = Tournament.load_all()
        for t in tournaments:
            if t.id == tournament_id:
                return t
        return None

    @staticmethod
    def delete_by_id(tournament_id):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != tournament_id]
        Tournament.save_all(tournaments)
