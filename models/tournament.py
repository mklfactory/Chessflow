import json
import uuid
from models.round import Round
from models.player import Player
from models.match import Match

TOURNAMENT_FILE = "data/tournaments.json"

class Tournament:
    def __init__(self, id=None, name="", location="", start_date="", end_date="", description="", total_rounds=4, current_round=0, rounds=None, players=None):
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
            "rounds": [r.id for r in self.rounds],
            "players": [p.id for p in self.players],
        }

    @classmethod
    def from_dict(cls, data):
        rounds = []
        for r_id in data.get("rounds", []):
            round_obj = Round.load_by_id(r_id)
            if round_obj:
                rounds.append(round_obj)
        players = []
        for p_id in data.get("players", []):
            player = Player.load_by_id(p_id)
            if player:
                players.append(player)
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
            players=players
        )

    def save(self):
        tournaments = Tournament.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]
        tournaments.append(self)
        with open(TOURNAMENT_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2, ensure_ascii=False)

    @classmethod
    def load_all(cls):
        try:
            with open(TOURNAMENT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [cls.from_dict(t) for t in data]
        except FileNotFoundError:
            return []

    @classmethod
    def load_by_id(cls, tournament_id):
        for t in cls.load_all():
            if t.id == tournament_id:
                return t
        return None

    @classmethod
    def delete(cls, tournament_id):
        tournaments = [t for t in cls.load_all() if t.id != tournament_id]
        with open(TOURNAMENT_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2, ensure_ascii=False)

    def add_player(self, player):
        if player.id not in [p.id for p in self.players]:
            self.players.append(player)

    def generate_pairings(self):
        import random
        if self.current_round == 0:
            players = self.players[:]
            random.shuffle(players)
        else:
            points = self.get_player_points()
            players = self.players[:]
            players.sort(key=lambda p: (points[p.id], random.random()), reverse=True)
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

        # Générer les appariements
        matches = self.generate_pairings()

        # Sauvegarder chaque match et récupérer les IDs
        match_ids = []
        for m in matches:
            m.save()
            match_ids.append(m.id)

        # Créer le round avec les IDs des matchs
        new_round = Round(name=round_name, match_ids=match_ids)
        Round.start_round(new_round)
        new_round.save()

        # Ajouter le round au tournoi et sauvegarder
        self.rounds.append(new_round)
        self.save()

        return new_round

    def get_player_points(self):
        points = {p.id: 0 for p in self.players}
        for round_obj in self.rounds:
            for match_id in round_obj.match_ids:
                match = Match.load_by_id(match_id)
                if match:
                    if match.player1_id in points: points[match.player1_id] += match.score1
                    if match.player2_id in points: points[match.player2_id] += match.score2
        return points
