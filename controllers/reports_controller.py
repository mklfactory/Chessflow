from models.tournament import Tournament
from models.player import Player
from views.reports_view import ReportView

class ReportsController:
    """
    Controller for generating and displaying reports using the ReportView.
    Handles reports related to players, tournaments, and rounds.
    """

    def __init__(self):
        """
        Initialize the ReportsController and its associated view.
        """
        self.view = ReportView()

    def run(self):
        """
        Main loop to display the report menu and handle user selections.
        """
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
        """
        Load all players, sort them alphabetically,
        and display the sorted list.
        """
        players = Player.load_all()
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        self.view.show_players_list(players_sorted)

    def list_all_tournaments(self):
        """
        Load all tournaments and display the list to the user.
        """
        tournaments = Tournament.load_all()
        self.view.show_tournament_list(tournaments)

    def list_players_for_tournament(self):
        """
        Display players registered for a specific tournament,
        sorted alphabetically.
        """
        tournament_id = self.view.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        players = [Player.load_by_id(pid) for pid in tournament.player_ids]
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        self.view.show_players_list(players_sorted)

    def show_rounds_and_matches(self):
        """
        Display rounds and matches for a selected tournament.
        """
        tournament_id = self.view.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        self.view.show_rounds_and_matches(tournament.rounds, tournament.name)
