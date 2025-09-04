from models.tournament import Tournament
from models.player import Player
from views.report_view import ReportView
from tabulate import tabulate

class ReportController:
    def __init__(self, interface):
        self.view = ReportView(interface)

    def run(self):
        while True:
            choice = self.view.display_report_menu()
            if choice == "1":
                self.list_all_players()
            elif choice == "2":
                self.list_all_tournaments()
            elif choice == "3":
                self.list_players_for_tournament()
            elif choice == "4":
                self.show_rounds_and_matches()
            elif choice == "0":
                break

    def list_all_players(self):
        players = Player.load_all()
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        self.view.show_players_list(players_sorted)

    def list_all_tournaments(self):
        tournaments = Tournament.load_all()
        self.view.show_tournament_list(tournaments)

    def list_players_for_tournament(self):
        tournament_id = self.view.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        players = [Player.load_by_id(pid) for pid in tournament.player_ids]
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        self.view.show_players_list(players_sorted)

    def show_rounds_and_matches(self):
        tournament_id = self.view.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        self.view.show_rounds(tournament.rounds, tournament.name)
        for round_obj in tournament.rounds:
            self.view.show_matches(round_obj.matches, round_obj.name)
