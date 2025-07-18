from models.tournament import Tournament
from views.tournament_view import TournamentView

class TournamentController:
    def __init__(self, interface):
        self.view = TournamentView(interface)

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
            elif choice == "0":
                break

    def add_tournament(self):
        data = self.view.ask_tournament_data()
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
        for key, value in data.items():
            setattr(tournament, key, value)
        tournament.save()
        self.view.show_message("Tournoi mis à jour.")

    def delete_tournament(self):
        tournament_id = self.view.ask_tournament_id()
        Tournament.delete(tournament_id)
        self.view.show_message("Tournoi supprimé.")
