from models.tournament import Tournament
from views.round_view import RoundView
from tabulate import tabulate
from datetime import datetime

class RoundController:
    """
    Controller for managing rounds in tournaments using the RoundView.
    Handles manual round creation, displaying rounds, entering match results, and showing standings.
    """

    def __init__(self):
        """
        Initialize the RoundController and its associated view.
        """
        self.view = RoundView()

    def ask_tournament_selection(self):
        """
        Display all available tournaments and ask the user to select one by ID.

        Returns:
            str: Selected tournament ID.
        """
        tournaments = Tournament.load_all()
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois disponibles :")
        print(tabulate(table, headers=["ID du tournoi", "Nom"], tablefmt="fancy_grid"))
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id

    def run(self):
        """
        Main loop to display the round menu and handle user actions.
        """
        while True:
            choice = self.view.display_round_menu()
            if choice == "1":
                self.create_manual_round()
            elif choice == "2":
                self.show_rounds()
            elif choice == "3":
                self.enter_results_manually()
            elif choice == "4":
                self.show_standings()
            elif choice == "0":
                break

    def create_manual_round(self):
        """
        Create a new round manually for the selected tournament.
        """
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        if tournament.current_round >= tournament.total_rounds:
            self.view.show_message("Tous les rounds ont déjà été créés.")
            return
        round_obj = tournament.create_next_round()
        if round_obj:
            round_obj.save()
            tournament.save()
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
        else:
            self.view.show_message("Impossible de créer un nouveau round.")

    def show_rounds(self):
        """
        Display all rounds for a selected tournament.
        """
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        self.view.show_rounds(tournament.rounds, tournament.name)

    def enter_results_manually(self):
        """
        Enter match results manually for a selected round of a tournament.
        """
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        if not tournament.rounds:
            self.view.show_message("Aucun round dans ce tournoi.")
            return
        self.view.show_rounds(tournament.rounds, tournament.name)
        round_id = self.view.ask_round_id()
        round_obj = next((r for r in tournament.rounds if r.id == round_id), None)
        if not round_obj:
            self.view.show_message("Round introuvable.")
            return
        for i, match in enumerate(round_obj.matches):
            self.view.show_match(match, i)
            score1, score2 = self.view.ask_scores()
            match.score1 = score1
            match.score2 = score2
            match.save()
        round_obj.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        round_obj.save()
        self.view.show_message(f"Résultats du {round_obj.name} mis à jour.")

    def show_standings(self):
        """
        Calculate and display standings for the selected tournament.
        """
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        points = self.calculate_points(tournament)
        self.view.show_standings(points)

    def calculate_points(self, tournament):
        """
        Calculate player points for a tournament.

        Args:
            tournament (Tournament): Tournament instance.

        Returns:
            dict: Mapping from player ID to points.
        """
        return tournament.get_player_points()
