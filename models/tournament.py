import json
import uuid
from random import shuffle, random
from models.round import Round
from models.player import Player
from models.match import Match

DATA_FILE = "data/tournaments.json"

class Tournament:
    def __init__(self, id=None, name="", location="", start_date="", end_date="", description="",
                 total_rounds=4, current_round=0, rounds=None, players=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.total_rounds = int(total_rounds or 4)
        self.current_round = int(current_round or 0)
        self.rounds = rounds or []      # liste d'objets Round
        self.players = players or []    # liste d'objets Player

    # ---------- Persistence ----------
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
        tournaments = self.load_all()
        tournaments = [t for t in tournaments if t.id != self.id]
        tournaments.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)

    @classmethod
    def load_all(cls):
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            return [cls.from_dict(t) for t in data]
        except Exception:
            return []

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
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=2)

    # ---------- Gestion Joueurs / Points ----------
    def add_player(self, player: Player):
        if player.id not in [p.id for p in self.players]:
            self.players.append(player)

    def get_player_points(self):
        points = {p.id: 0.0 for p in self.players}
        for round_obj in self.rounds:
            for m in round_obj.matches:
                if m.player1:
                    points[m.player1.id] += float(m.score1)
                if m.player2:
                    points[m.player2.id] += float(m.score2)
        return points

    # ---------- Génération des appariements ----------
    def _already_played(self, p1_id, p2_id):
        for r in self.rounds:
            for m in r.matches:
                ids = {m.player1.id if m.player1 else None, m.player2.id if m.player2 else None}
                if p1_id in ids and p2_id in ids:
                    return True
        return False

    def generate_pairings(self):
        # Round 1 : tirage/mélange aléatoire
        if self.current_round == 0:
            players = self.players[:]
            shuffle(players)
        else:
            # trier par points (desc), puis aléatoire pour briser les égalités
            pts = self.get_player_points()
            players = sorted(self.players, key=lambda p: (pts[p.id], random()), reverse=True)

        pairings = []
        used = set()
        i = 0
        while i < len(players):
            p1 = players[i]
            if p1.id in used:
                i += 1
                continue

            opponent = None
            # chercher un adversaire jamais rencontré si possible
            for j in range(i+1, len(players)):
                p2 = players[j]
                if p2.id not in used and not self._already_played(p1.id, p2.id):
                    opponent = p2
                    break

            # sinon, prendre le prochain dispo
            if opponent is None:
                for j in range(i+1, len(players)):
                    p2 = players[j]
                    if p2.id not in used:
                        opponent = p2
                        break

            if opponent:
                pairings.append(Match(p1, opponent))
                used.add(p1.id); used.add(opponent.id)
            else:
                # joueur impair -> bye
                pairings.append(Match(p1, None))
                used.add(p1.id)
            i += 1

        return pairings

    def create_next_round(self):
        if self.current_round >= self.total_rounds:
            return None
        self.current_round += 1
        round_name = f"Round {self.current_round}"
        matches = self.generate_pairings()
        new_round = Round(name=round_name, matches=matches)
        Round.start_round(new_round)
        self.rounds.append(new_round)
        self.save()
        return new_round

    # ---------- Rapports ----------
    def report_players(self):
        return Player.sort_alphabetically(self.players)

    def report_rounds(self):
        return self.rounds

    def report_matches(self):
        return [(r.name, r.matches) for r in self.rounds]
