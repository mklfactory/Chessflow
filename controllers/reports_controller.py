# Importing the Tournament and Player models, and the ReportView for displaying reports
from models.tournament import Tournament
from models.player import Player
from views.reports_view import ReportView


class ReportsController:
 
    def __init__(self, interface):
        # Initialize the ReportView with the main interface
        self.view = ReportView(interface)
    
    def run(self):
        # Main loop for managing reports
        while True:
            # Display the report menu and get the user's choice
            choice = self.view.display_report_menu()
            if choice == "1":
                self.list_all_players()  # List all players
            elif choice == "2":
                self.list_all_tournaments()  # List all tournaments
            elif choice == "3":
                self.list_players_for_tournament()  # List players for a specific tournament
            elif choice == "4":
                self.show_rounds_and_matches()  # Show rounds and matches for a tournament
            elif choice == "0":
                # Exit the report management menu
                break
       
    def list_all_players(self):
        # Load all players from the database or storage
        players = Player.load_all()
        # Sort players alphabetically by last name and first name
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        # Display the sorted list of players
        self.view.show_players_list(players_sorted)
     
    def list_all_tournaments(self):
        # Load all tournaments from the database or storage
        tournaments = Tournament.load_all()
        # Display the list of tournaments
        self.view.show_tournament_list(tournaments)
      
    def list_players_for_tournament(self):
        # Ask the user to select a tournament by ID
        tournament_id = self.view.ask_tournament_selection()
        # Load the tournament by ID
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Load players for the selected tournament
        players = [Player.load_by_id(pid) for pid in tournament.player_ids]
        # Sort players alphabetically by last name and first name
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        # Display the sorted list of players
        self.view.show_players_list(players_sorted)
     
    def show_rounds_and_matches(self):
        # Ask the user to select a tournament by ID
        tournament_id = self.view.ask_tournament_selection()
        # Load the tournament by ID
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Display the rounds and matches for the selected tournament
        self.view.show_rounds_and_matches(tournament.rounds, tournament.name)
