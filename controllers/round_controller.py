from models.tournament import Tournament
from views.round_view import RoundView
from tabulate import tabulate
from datetime import datetime

class RoundController:
    def __init__(self, interface):
        # Initialize the RoundView with the main interface
        self.view = RoundView(interface)
    def ask_tournament_selection(self):
        # Load all tournaments from the database or storage
        tournaments = Tournament.load_all()
        # Display a table of available tournaments
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois disponibles :")
        print(tabulate(table, headers=["ID du tournoi", "Nom"], tablefmt="fancy_grid"))
        # Ask the user to select a tournament by ID
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id
    def run(self):
        # Main loop for managing rounds
        while True:
            # Display the round menu and get the user's choice
            choice = self.view.display_round_menu()
            if choice == "1":
                self.create_manual_round()  # Create a new round manually
            elif choice == "2":
                self.show_rounds()  # Show all rounds for a tournament
            elif choice == "3":
                self.enter_results_manually()  # Enter match results manually
            elif choice == "4":
                self.show_standings()  # Show tournament standings
            elif choice == "0":
                # Exit the round management menu
                break
    def create_manual_round(self):
        # Ask the user to select a tournament
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        if tournament.current_round >= tournament.total_rounds:
            # Notify the user if all rounds have already been created
            self.view.show_message("Tous les rounds ont déjà été créés.")
            return
        # Create the next round for the tournament
        round_obj = tournament.create_next_round()
        if round_obj:
            # Save the round and the tournament
            round_obj.save()
            tournament.save()
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
        else:
            # Notify the user if the round could not be created
            self.view.show_message("Impossible de créer un nouveau round.")
    def show_rounds(self):
        # Ask the user to select a tournament
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Display all rounds for the selected tournament
        self.view.show_rounds(tournament.rounds, tournament.name)
    def enter_results_manually(self):
        # Ask the user to select a tournament
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        if not tournament.rounds:
            # Notify the user if there are no rounds in the tournament
            self.view.show_message("Aucun round dans ce tournoi.")
            return
        # Display all rounds for the selected tournament
        self.view.show_rounds(tournament.rounds, tournament.name)
        # Ask the user to select a round by ID
        round_id = self.view.ask_round_id()
        round_obj = next((r for r in tournament.rounds if r.id == round_id), None)
        if not round_obj:
            # Notify the user if the round is not found
            self.view.show_message("Round introuvable.")
            return
        # Iterate through the matches in the round and ask for scores
        for i, match in enumerate(round_obj.matches):
            self.view.show_match(match, i)
            score1, score2 = self.view.ask_scores()
            match.score1 = score1
            match.score2 = score2
            match.save()
        # Update the round's end time and save it
        round_obj.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        round_obj.save()
        self.view.show_message(f"Résultats du {round_obj.name} mis à jour.")
    def show_standings(self):
        # Ask the user to select a tournament
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Calculate the standings for the tournament
        points = self.calculate_points(tournament)
        # Display the standings
        self.view.show_standings(points)
    def calculate_points(self, tournament):
        # Initialize a dictionary to store points for each player
        points = {pid: 0.0 for pid in tournament.player_ids}
        # Iterate through the rounds and matches to calculate points
        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                if match.player1_id is not None:
                    points[match.player1_id] += match.score1
                if match.player2_id is not None:
                    points[match.player2_id] += match.score2
        return points
