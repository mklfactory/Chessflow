# Importing controllers for different parts of the application
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController
from controllers.player_controller import PlayerController
from controllers.reports_controller import ReportsController

# Importing the view for the main interface
from views.main_view import MainView


class MainController:
    def __init__(self):
        # Initialize the main interface view
        self.interface = MainView()
        # Initialize controllers for tournaments, rounds, players, and reports
        self.tournament_controller = TournamentController(self.interface)
        self.round_controller = RoundController(self.interface)
        self.player_controller = PlayerController(self.interface)
        self.reports_controller = ReportsController(self.interface)

    def run(self):
        # Main application loop
        while True:
            # Display the main menu and get the user's choice
            choice = self.interface.display_main_menu()
            # Handle the user's choice by delegating to the appropriate controller
            if choice == "1":
                self.tournament_controller.run()  # Manage tournaments
            elif choice == "2":
                self.round_controller.run()  # Manage rounds
            elif choice == "3":
                self.player_controller.run()  # Manage players
            elif choice == "4":
                self.reports_controller.run()  # Generate reports
            elif choice == "0":
                # Exit the application
                print("À bientôt 👋")
                break
            else:
                # Handle invalid choices
                print("Choix invalide.")
                