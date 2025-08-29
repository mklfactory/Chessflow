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
                self.list_all_players()
            elif choice == "2":
                self.list_all_tournaments()
            elif choice == "3":
                self.tournament_info()
            elif choice == "4":
                self.tournament_players_alpha()
            elif choice == "5":
                self.tournament_rounds_matches()
            elif choice == "0":
                break
            else:
                self.view.show_message("Choix invalide.")

    def list_all_players(self):
        players = Player.load_all()
        self.view.show_players(Player.sort_alphabetically(players))

    def list_all_tournaments(self):
        tournaments = Tournament.load_all()
        self.view.show_tournaments(tournaments)

    def tournament_info(self):
        t = self._get_tournament_or_msg()
        if t:
            self.view.show_tournament_info(t)

    def tournament_players_alpha(self):
        t = self._get_tournament_or_msg()
        if t:
            self.view.show_players(Player.sort_alphabetically(t.players))

    def tournament_rounds_matches(self):
        t = self._get_tournament_or_msg()
        if not t:
            return
        for r in t.rounds:
            self.view.show_round_summary(r)
            for i, m in enumerate(r.matches):
                self.view.show_match_detail(i+1, m)

    def _get_tournament_or_msg(self):
        tid = self.view.ask_tournament_id()
        t = Tournament.load_by_id(tid)
        if not t:
            self.view.show_message("Tournoi introuvable.")
            return None
        return t
