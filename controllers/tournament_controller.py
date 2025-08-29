from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.round_view import RoundView

class TournamentController:
    def __init__(self, interface):
        self.view = TournamentView(interface)
        self.round_view = RoundView(interface)

    def run(self):
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.add_tournament()
            elif choice == "2":
                self.list_tournaments()
            elif choice == "3":
                self.update_tournament()
            elif choice == "4":
                self.delete_tournament()
            elif choice == "5":
                self.manage_tournament()
            elif choice == "0":
                break

    def add_tournament(self):
        data = self.view.ask_tournament_data()
        # Correction : renommer total_rounds -> number_of_rounds
        if 'total_rounds' in data:
            data['number_of_rounds'] = data.pop('total_rounds')
        tournament = Tournament(**data)
        tournament.save()
        self.view.show_message("Tournoi ajouté.")

    def list_tournaments(self):
        tournaments = Tournament.load_all()
        self.view.show_tournaments(tournaments)

    def update_tournament(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        data = self.view.ask_tournament_data()
        # Même correction pour update
        if 'total_rounds' in data:
            data['number_of_rounds'] = data.pop('total_rounds')
        for key, value in data.items():
            setattr(tournament, key, value)
        tournament.save()
        self.view.show_message("Tournoi mis à jour.")

    def delete_tournament(self):
        tournament_id = self.view.ask_tournament_id()
        Tournament.delete(tournament_id)
        self.view.show_message("Tournoi supprimé.")

    def manage_tournament(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        while True:
            choice = self.view.display_manage_menu()
            if choice == "1":
                self.add_player_to_tournament(tournament)
            elif choice == "2":
                self.list_tournament_players(tournament)
            elif choice == "3":
                self.create_next_round(tournament)
            elif choice == "4":
                self.list_rounds_and_matches(tournament)
            elif choice == "0":
                break

    def add_player_to_tournament(self, tournament):
        player_id = self.view.ask_player_id()
        player = Player.load_by_id(player_id)
        if not player:
            self.view.show_message("Joueur introuvable.")
            return
        tournament.add_player(player)
        tournament.save()
        self.view.show_message(f"Joueur {player.full_name()} ajouté au tournoi.")

    def list_tournament_players(self, tournament):
        players_sorted = Player.sort_alphabetically(tournament.players)
        self.view.show_players(players_sorted)

    def create_next_round(self, tournament):
        round_obj = tournament.create_next_round()
        if round_obj:
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
        else:
            self.view.show_message("Tournoi déjà terminé.")

    def list_rounds_and_matches(self, tournament):
        for r in tournament.rounds:
            self.view.show_round_summary(r)
            for i, m in enumerate(r.matches):
                self.view.show_match_detail(i+1, m)
