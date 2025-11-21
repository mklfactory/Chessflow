from models.player import Player
from tabulate import tabulate

class RoundView:
    """
    View component for round management, providing formatted console output for rounds, matches, and standings.
    """

    def __init__(self, interface):
        """
        Initialize the RoundView instance.

        Args:
            interface: The main application interface.
        """
        pass

    def display_round_menu(self):
        """
        Display the round management menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        menu = [
            ["1", "Créer un round manuellement"],
            ["2", "Voir les rounds"],
            ["3", "Saisir les résultats manuellement"],
            ["4", "Voir le classement"],
            ["0", "Retour"]
        ]
        print("\n--- Gestion des Rounds ---")
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        return input("Votre choix : ")

    def ask_round_id(self):
        """
        Prompt the user to input a round ID.

        Returns:
            str: Round ID input by the user.
        """
        return input("ID du round : ")

    def show_tournament_list(self, tournaments):
        """
        Display a table of available tournaments.

        Args:
            tournaments (list): List of Tournament instances.
        """
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois disponibles :")
        print(tabulate(table, headers=["ID du Tournoi", "Nom"], tablefmt="fancy_grid"))

    def show_rounds(self, rounds, tournament_name=None):
        """
        Display a table listing all rounds for a tournament.

        Args:
            rounds (list): List of Round instances.
            tournament_name (str, optional): Name of the tournament.
        """
        title = "--- Gestion des Rounds ---"
        if tournament_name:
            title += f" (Tournoi : {tournament_name})"
        print(title)
        headers = ["ID", "Nom", "Début", "Fin"]
        data = [[r.id, r.name, r.start_time or "", r.end_time or ""] for r in rounds]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_match(self, match, index):
        """
        Display details of a specific match.

        Args:
            match: Match instance to display.
            index (int): Index of the match in the list.
        """
        p1 = Player.load_by_id(match.player1_id)
        p2 = Player.load_by_id(match.player2_id)
        name1 = p1.full_name() if p1 else "Bye"
        name2 = p2.full_name() if p2 else "Bye"
        print(f"Match {index + 1}: {name1} vs {name2} (Current scores: {match.score1} - {match.score2})")

    def ask_scores(self):
        """
        Prompt the user to input scores for both players in a match.

        Returns:
            tuple: (score1, score2) entered by the user.
        """
        while True:
            try:
                score1 = float(input("Joueur 1 score: "))
                score2 = float(input("Joueur 2 score: "))
                if score1 < 0 or score2 < 0:
                    print("Les scores doivent être positifs.")
                    continue
                return score1, score2
            except ValueError:
                print("Entrée invalide, veuillez entrer un nombre.")

    def show_standings(self, points):
        """
        Display the current standings in a table format.

        Args:
            points (dict): Mapping from player ID to score.
        """
        headers = ["Joueur", "Points"]
        data = []
        for player_id, score in sorted(points.items(), key=lambda x: x[1], reverse=True):
            player = Player.load_by_id(player_id)
            name = player.full_name() if player else player_id
            data.append([name, score])
        print("\nClassement actuel:")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_message(self, msg):
        """
        Display an informational message.

        Args:
            msg (str): The message to display.
        """
        print(f"[INFO] {msg}")
