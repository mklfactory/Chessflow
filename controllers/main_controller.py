from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController
from controllers.player_controller import PlayerController
from controllers.reports_controller import ReportsController
from views.main_view import MainView

class MainController:
    """
    Main controller that coordinates the application's interface and delegates functionality
    to dedicated controllers for tournaments, rounds, players, and reports.
    """

    def __init__(self):
        """
        Initialize the main controller and all sub-controllers.
        """
        self.interface = MainView()
        self.tournament_controller = TournamentController()
        self.round_controller = RoundController()
        self.player_controller = PlayerController()
        self.reports_controller = ReportsController()

    def run(self):
        """
        Main application loop. Displays the menu and delegates actions to the corresponding controller
        based on user selection.
        """
        while True:
            choice = self.interface.display_main_menu()
            if choice == "1":
                self.tournament_controller.run()
            elif choice == "2":
                self.round_controller.run()
            elif choice == "3":
                self.player_controller.run()
            elif choice == "4":
                self.reports_controller.run()
            elif choice == "0":
                print("À bientôt 👋")
                break
            else:
                print("Choix invalide.")
