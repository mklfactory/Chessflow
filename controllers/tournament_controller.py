from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.round_view import RoundView


class TournamentController:
    def __init__(self, interface):
        # Initialize the TournamentView and RoundView with the main interface
        self.view = TournamentView(interface)
        self.round_view = RoundView(interface)

    def ask_tournament_selection(self):
        # Load all tournaments from the database or storage
        tournaments = Tournament.load_all()
        print("Liste des tournois disponibles :")
        # Display the list of tournaments
        for t in tournaments:
            print(f"{t.id} - {t.name}")
        # Ask the user to select a tournament by ID
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id

    def run(self):
        # Main loop for managing tournaments
        while True:
            # Display the tournament menu and get the user's choice
            choice = self.view.display_menu()
            if choice == "1":
                self.add_tournament()  # Add a new tournament
            elif choice == "2":
                self.list_tournaments()  # List all tournaments
            elif choice == "3":
                self.update_tournament()  # Update an existing tournament
            elif choice == "4":
                self.delete_tournament()  # Delete a tournament
            elif choice == "5":
                self.manage_tournament()  # Manage a specific tournament
            elif choice == "0":
                # Exit the tournament management menu
                break

    def add_tournament(self):
        # Collect tournament data from the user
        data = self.view.ask_tournament_data()
        # Create a new Tournament instance with the provided data
        tournament = Tournament(**data)
        # Save the tournament to the database or storage
        tournament.save()
        # Notify the user that the tournament was added
        self.view.show_message("Tournoi ajouté.")

    def list_tournaments(self):
        # Load all tournaments from the database or storage
        tournaments = Tournament.load_all()
        # Display the list of tournaments
        self.view.show_tournaments(tournaments)

    def update_tournament(self):
        # Ask the user to select a tournament by ID
        tournament_id = self.ask_tournament_selection()
        # Load the tournament by ID
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Collect updated tournament data from the user
        data = self.view.ask_tournament_data()
        # Update the tournament's attributes with the new data
        for key, value in data.items():
            setattr(tournament, key, value)
        # Save the updated tournament to the database or storage
        tournament.save()
        # Notify the user that the tournament was updated
        self.view.show_message("Tournoi mis à jour.")

    def delete_tournament(self):
        # Ask the user to select a tournament by ID
        tournament_id = self.ask_tournament_selection()
        # Delete the tournament from the database or storage
        Tournament.delete(tournament_id)
        # Notify the user that the tournament was deleted
        self.view.show_message("Tournoi supprimé.")

    def manage_tournament(self):
        # Ask the user to select a tournament by ID
        tournament_id = self.ask_tournament_selection()
        # Load the tournament by ID
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            # Notify the user if the tournament is not found
            self.view.show_message("Tournoi introuvable.")
            return
        # Loop for managing the selected tournament
        while True:
            # Display the tournament management menu and get the user's choice
            choice = self.view.display_manage_menu()
            if choice == "1":
                self.add_player_to_tournament(tournament)  # Add a player to the tournament
            elif choice == "2":
                self.list_tournament_players(tournament)  # List players in the tournament
            elif choice == "3":
                self.create_next_round(tournament)  # Create the next round
            elif choice == "4":
                self.list_rounds_and_matches(tournament)  # List rounds and matches
            elif choice == "5":
                self.generate_report(tournament)  # Generate a tournament report
            elif choice == "0":
                # Exit the tournament management menu
                break

    def add_player_to_tournament(self, tournament):
        # Ask the user for the ID of the player to add
        player_id = self.view.ask_player_id()
        # Load the player by ID
        player = Player.load_by_id(player_id)
        if not player:
            # Notify the user if the player is not found
            self.view.show_message("Joueur introuvable.")
            return
        # Add the player to the tournament
        tournament.add_player(player)
        # Save the updated tournament
        tournament.save()
        # Notify the user that the player was added
        self.view.show_message(f"Joueur {player.full_name()} ajouté au tournoi.")

    def list_tournament_players(self, tournament):
        # Load players in the tournament
        players = [Player.load_by_id(pid) for pid in tournament.player_ids if Player.load_by_id(pid)]
        # Sort players alphabetically
        players_sorted = Player.sort_alphabetically(players)
        # Display the sorted list of players
        self.view.show_players(players_sorted)

    def create_next_round(self, tournament):
        # Check if all rounds have already been created
        if tournament.current_round >= tournament.total_rounds:
            self.view.show_message("Tournoi déjà terminé.")
            return
        # Create the next round for the tournament
        round_obj = tournament.create_next_round()
        if round_obj:
            # Notify the user that the round was created
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
            # Save the round
            round_obj.save()
        else:
            # Notify the user if the round could not be created
            self.view.show_message("Impossible de créer un nouveau round.")

    def list_rounds_and_matches(self, tournament):
        # Display all rounds and their matches for the tournament
        for r in tournament.rounds:
            self.view.show_round_summary(r)
            for i, m in enumerate(r.matches):
                self.view.show_match_detail(i + 1, m)

    def generate_report(self, tournament):
        import json
        # Generate a report containing tournament, rounds, and players data
        report = {
            "tournament": tournament.to_dict(),
            "rounds": [r.to_dict() for r in tournament.rounds],
            "players": [p.to_dict()
                        for p in [
                            Player.load_by_id(pid)
                            for pid in tournament.player_ids
                            if Player.load_by_id(pid)]]
        }
        try:
            # Save the report to a JSON file
            with open("data/reports.json", "w") as f:
                json.dump(report, f, indent=2)
            # Notify the user that the report was generated
            self.view.show_message("Rapport généré dans data/reports.json")
        except Exception as e:
            # Notify the user if an error occurred during report generation
            self.view.show_message(f"Erreur lors de la génération du rapport : {e}")
