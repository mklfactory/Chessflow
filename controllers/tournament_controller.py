from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.round_view import RoundView

class TournamentController:
    """
    Controller for managing tournaments, rounds, and tournament-related actions using the corresponding views.
    Handles creation, listing, updating, and deletion of tournaments, as well as player management and reporting.
    """

    def __init__(self, interface):
        """
        Initialize the TournamentController and its associated views.

        Args:
            interface: The main application interface for the views.
        """
        self.view = TournamentView(interface)
        self.round_view = RoundView(interface)

    def ask_tournament_selection(self):
        """
        Display all available tournaments and prompt the user to select one by ID.

        Returns:
            str: Selected tournament ID.
        """
        tournaments = Tournament.load_all()
        print("Liste des tournois disponibles :")
        for t in tournaments:
            print(f"{t.id} - {t.name}")
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id

    def run(self):
        """
        Main loop to display the tournament menu and handle user actions.
        """
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
            elif choice == "5":
                self.manage_tournament()
            elif choice == "0":
                break

    def add_tournament(self):
        """
        Collect tournament data, create a new Tournament,
        save it, and notify the user.
        """
        data = self.view.ask_tournament_data()
        tournament = Tournament(**data)
        tournament.save()
        self.view.show_message("Tournoi ajouté.")

    def list_tournaments(self):
        """
        Load all tournaments and display them to the user.
        """
        tournaments = Tournament.load_all()
        self.view.show_tournaments(tournaments)

    def update_tournament(self):
        """
        Update an existing tournament's information and notify the user.
        """
        tournament_id = self.ask_tournament_selection()
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
        """
        Delete a tournament by its ID and notify the user.
        """
        tournament_id = self.ask_tournament_selection()
        Tournament.delete(tournament_id)
        self.view.show_message("Tournoi supprimé.")

    def manage_tournament(self):
        """
        Loop for managing a selected tournament,
        including player management, rounds, and reporting.
        """
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        while True:
            choice = self.view.display_manage_menu()
            if choice == "1":
                self.add_player_to_tournament(tournament)
            elif choice == "2":
                self.list_tournament_players(tournament)
            elif choice == "3":
                self.create_next_round(tournament)
            elif choice == "4":
                self.list_rounds_and_matches(tournament)
            elif choice == "5":
                self.generate_report(tournament)
            elif choice == "0":
                break

    def add_player_to_tournament(self, tournament):
        """
        Add a player to the tournament after verifying their existence.
        """
        player_id = self.view.ask_player_id()
        player = Player.load_by_id(player_id)
        if not player:
            self.view.show_message("Joueur introuvable.")
            return
        tournament.add_player(player)
        tournament.save()
        self.view.show_message(f"Joueur {player.full_name()} ajouté au tournoi.")

    def list_tournament_players(self, tournament):
        """
        Load and display all players in the tournament, sorted alphabetically.
        """
        players = [Player.load_by_id(pid) for pid in tournament.player_ids if Player.load_by_id(pid)]
        players_sorted = Player.sort_alphabetically(players)
        self.view.show_players(players_sorted)

    def create_next_round(self, tournament):
        """
        Attempt to create the next round of the tournament and notify the user.
        """
        if tournament.current_round >= tournament.total_rounds:
            self.view.show_message("Tournoi déjà terminé.")
            return
        round_obj = tournament.create_next_round()
        if round_obj:
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
            round_obj.save()
        else:
            self.view.show_message("Impossible de créer un nouveau round.")

    def list_rounds_and_matches(self, tournament):
        """
        Display all rounds and their matches for the tournament.
        """
        for r in tournament.rounds:
            self.view.show_round_summary(r)
            for i, m in enumerate(r.matches):
                self.view.show_match_detail(i + 1, m)

    def generate_report(self, tournament):
        """
        Generate a JSON report for the tournament, rounds, and players,
        and notify the user upon success or error.
        """
        import json
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
            with open("data/reports.json", "w") as f:
                json.dump(report, f, indent=2)
            self.view.show_message("Rapport généré dans data/reports.json")
        except Exception as e:
            self.view.show_message(f"Erreur lors de la génération du rapport : {e}")
