from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController
from controllers.player_controller import PlayerController
from controllers.reports_controller import ReportsController
from views.main_view import MainView

class MainController:
    def __init__(self):
        self.interface = MainView()
        self.tournament_controller = TournamentController(self.interface)
        self.round_controller = RoundController(self.interface)
        self.player_controller = PlayerController(self.interface)
        self.reports_controller = ReportsController(self.interface)

    def run(self):
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
