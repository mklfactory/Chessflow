from models.round import Round
from models.match import Match
from models.player import Player
import json
import uuid

TOURNAMENT_FILE = "data/tournaments.json"

class Tournament:
    def __init__(self, id=None, name="", location="", start_date="", end_date="", description="", total_rounds=4, current_round=0, round_ids=None, player_ids=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.total_rounds = total_rounds
        self.current_round = current_round
        self.round_ids = round_ids or []
        self.player_ids = player_ids or []

    @property
    def rounds(self):
        return [Round.load_by_id(rid) for rid in self.round_ids]

    @property
    def players(self):
        return [Player.load_by_id(pid) for pid in self.player_ids]

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
            "round_ids": self.round_ids,
            "player_ids": self.player_ids
        }

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]
        tournaments.append(self)
        with open(TOURNAMENT_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=4)

    @classmethod
    def load_all(cls):
        try:
            with open(TOURNAMENT_FILE, "r") as f:
                data = json.load(f)
            return [cls(**t) for t in data]
        except FileNotFoundError:
            return []

    @classmethod
    def load_by_id(cls, tournament_id):
        for t in cls.load_all():
            if t.id == tournament_id:
                return t
        return None

    def add_player(self, player):
        if player.id not in self.player_ids:
            self.player_ids.append(player.id)
            self.save()

    def generate_pairings(self):
        import random
        players = self.players[:]
        random.shuffle(players)
        pairings = []
        used = set()
        i = 0
        while i < len(players):
            p1 = players[i]
            if p1.id in used:
                i += 1
                continue
            opponent = None
            for j in range(i + 1, len(players)):
                p2 = players[j]
                if p2.id not in used:
                    opponent = p2
                    break
            match = Match(player1_id=p1.id, player2_id=opponent.id if opponent else None)
            match.save()
            pairings.append(match)
            used.add(p1.id)
            if opponent:
                used.add(opponent.id)
            i += 1
        return pairings

    def create_next_round(self):
        if self.current_round >= self.total_rounds:
            return None
        self.current_round += 1
        round_name = f"Round {self.current_round}"
        matches = self.generate_pairings()
        new_round = Round(name=round_name)
        for m in matches:
            new_round.add_match(m)
        new_round.save()
        self.round_ids.append(new_round.id)
        self.save()
        return new_round

    def get_player_points(self):
        points = {p.id: 0 for p in self.players}
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if match.player1_id:
                    points[match.player1_id] += match.score1
                if match.player2_id:
                    points[match.player2_id] += match.score2
        return points
