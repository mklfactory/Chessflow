from models.tournament import Tournament
from models.player import Player
from views.reports_view import ReportsView


class ReportsController:
    def __init__(self, interface):
        self.view = ReportsView(interface)

    def run(self):
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.all_players_alpha()
            elif choice == "2":
                self.all_tournaments()
            elif choice == "3":
                self.tournament_players_alpha()
            elif choice == "4":
                self.tournament_rounds_and_matches()
            elif choice == "0":
                break

    def all_players_alpha(self):
        players = Player.load_all()
        players_sorted = Player.sort_alphabetically(players)
        self.view.show_players(players_sorted)

    def all_tournaments(self):
        tournaments = Tournament.load_all()
        self.view.show_tournaments(tournaments)

    def tournament_players_alpha(self):
        tournament_id = self.view.ask_tournament_id()
        t = Tournament.load_by_id(tournament_id)
        if not t:
            self.view.show_message("Tournoi introuvable.")
            return
        players = [Player.load_by_id(pid) for pid in t.player_ids]
        players = [p for p in players if p]
        players_sorted = Player.sort_alphabetically(players)
        self.view.show_players(players_sorted)

    def tournament_rounds_and_matches(self):
        tournament_id = self.view.ask_tournament_id()
        t = Tournament.load_by_id(tournament_id)
        if not t:
            self.view.show_message("Tournoi introuvable.")
            return
        for r in t.get_rounds():
            self.view.show_round_summary(r)
            for i, m in enumerate(r.get_matches()):
                self.view.show_match_detail(i + 1, m)
