from tabulate import tabulate
from models.player import Player

class ReportView:
    """
    View component for displaying reports, listings, and round/match details in a formatted table.
    """

    def __init__(self, interface):
        """
        Initialize the ReportView instance.

        Args:
            interface: The main application interface.
        """
        pass

    def display_report_menu(self):
        """
        Display the report menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        menu = [
            ["1", "Liste de tous les joueurs (par ordre alphabétique)"],
            ["2", "Liste de tous les tournois"],
            ["3", "Joueurs d'un tournoi (par ordre alphabétique)"],
            ["4", "Rounds et matchs d'un tournoi"],
            ["0", "Retour"]
        ]
        print("\n--- Rapports ---")
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        return input("Votre choix : ")

    def show_players_list(self, players):
        """
        Display a table listing all players.

        Args:
            players (list): List of Player instances.
        """
        table = [[p.id, f"{p.last_name} {p.first_name}", p.birth_date] for p in players]
        print("Liste des joueurs :")
        print(tabulate(table, headers=["ID", "Nom", "Date de Naissance"], tablefmt="fancy_grid"))

    def show_tournament_list(self, tournaments):
        """
        Display a table listing all tournaments.

        Args:
            tournaments (list): List of Tournament instances.
        """
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois :")
        print(tabulate(table, headers=["ID", "Nom"], tablefmt="fancy_grid"))

    def ask_tournament_selection(self):
        """
        Prompt the user to input a tournament ID.

        Returns:
            str: Tournament ID input by the user.
        """
        tournament_id = input("ID du Tournoi : ")
        return tournament_id

    def show_rounds_and_matches(self, rounds, tournament_name=None):
        """
        Display rounds and associated matches for a tournament.

        Args:
            rounds (list): List of Round instances.
            tournament_name (str, optional): Name of the tournament.
        """
        print(f"\nRounds et matchs du tournoi : {tournament_name}")
        for r in rounds:
            print(f"\n{r.name} - Début : {r.start_time or '—'} | Fin : {r.end_time or '—'}")
            table = []
            for i, match in enumerate(r.matches, 1):
                p1 = Player.load_by_id(match.player1_id)
                p2 = Player.load_by_id(match.player2_id)
                name1 = p1.full_name() if p1 else "Bye"
                name2 = p2.full_name() if p2 else "Bye"
                table.append([f"Match {i}", f"{name1} ({match.score1})", f"{name2} ({match.score2})"])
            print(tabulate(table, headers=["Match", "Joueur 1 (Score)", "Joueur 2 (Score)"], tablefmt="fancy_grid"))

    def show_message(self, msg):
        """
        Display an informational message in the console.

        Args:
            msg (str): The message to display.
        """
        print(f"[INFO] {msg}")
