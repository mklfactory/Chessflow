import json
from models.tournament import Tournament
from models.player import Player
from views.view import View


class TournamentController:
    def __init__(self):
        self.view = View()
        self.players = self.load_players()
        self.tournaments = self.load_tournaments()

    def run(self):
        while True:
            choice = self.view.main_menu()
            if choice == "1":
                self.add_player()
            elif choice == "2":
                self.create_tournament()
            elif choice == "3":
                self.list_tournaments()
            elif choice == "4":
                self.view.display("Au revoir !")
                break

    def add_player(self):
        data = self.view.get_player_info()
        new_player = Player(*data)
        self.players.append(new_player)
        self.save_players()
        self.view.display("Joueur ajouté avec succès.")

    def create_tournament(self):
        data = self.view.get_tournament_info()
        selected_players = self.players[:8]  # simplifié pour la démo
        tournament = Tournament(*data, players=selected_players)
        self.tournaments.append(tournament)
        self.save_tournaments()
        self.view.display("Tournoi créé avec succès.")

    def list_tournaments(self):
        for t in self.tournaments:
            self.view.display(str(t))

    def save_players(self):
        with open("data/players.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.players], f, indent=4)

    def load_players(self):
        try:
            with open("data/players.json", "r", encoding="utf-8") as f:
                return [Player.from_dict(p) for p in json.load(f)]
        except FileNotFoundError:
            return []

    def save_tournaments(self):
        with open("data/tournaments.json", "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tournaments], f, indent=4)

    def load_tournaments(self):
        try:
            with open("data/tournaments.json", "r", encoding="utf-8") as f:
                return [Tournament.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            return []
