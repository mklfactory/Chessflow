from models.player import Player
from tabulate import tabulate


class RoundView:
    def __init__(self, interface):
        # Initialize the RoundView class
        pass

    def display_round_menu(self):
        # Display the round management menu with options
        menu = [
            ["1", "Créer un round manuellement"],
            ["2", "Voir les rounds"],
            ["3", "Saisir les résultats manuellement"],
            ["4", "Voir le classement"],
            ["0", "Retour"]
        ]
        print("\n--- Gestion des Rounds ---")
        # Print the menu using the tabulate library for formatting
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        # Return the user's choice
        return input("Votre choix : ")

    def ask_round_id(self):
        # Prompt the user to input a round ID
        return input("ID du round : ")

    def show_tournament_list(self, tournaments):
        # Display a list of available tournaments in a table format
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois disponibles :")
        print(tabulate(table, headers=["ID du Tournoi", "Nom"], tablefmt="fancy_grid"))

    def show_rounds(self, rounds, tournament_name=None):
        # Display a list of rounds for a tournament
        title = "--- Gestion des Rounds ---"
        if tournament_name:
            # Include the tournament name in the title if provided
            title += f" (Tournoi : {tournament_name})"
        print(title)
        # Define table headers and data
        headers = ["ID", "Nom", "Début", "Fin"]
        data = [[r.id, r.name, r.start_time or "", r.end_time or ""] for r in rounds]
        # Print the table of rounds
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_match(self, match, index):
        # Display details of a specific match
        p1 = Player.load_by_id(match.player1_id)  # Load player 1 details
        p2 = Player.load_by_id(match.player2_id)  # Load player 2 details
        name1 = p1.full_name() if p1 else "Bye"  # Player 1 name or "Bye"
        name2 = p2.full_name() if p2 else "Bye"  # Player 2 name or "Bye"
        # Print match details with current scores
        print(f"Match {index + 1}: {name1} vs {name2} (Current scores: {match.score1} - {match.score2})")

    def ask_scores(self):
        # Prompt the user to input scores for a match
        while True:
            try:
                score1 = float(input("Joueur 1 score: "))  # Input score for player 1
                score2 = float(input("Joueur 2 score: "))  # Input score for player 2
                if score1 < 0 or score2 < 0:
                    # Ensure scores are non-negative
                    print("Les scores doivent être positifs.")
                    continue
                return score1, score2
            except ValueError:
                # Handle invalid input
                print("Entrée invalide, veuillez entrer un nombre.")

    def show_standings(self, points):
        # Display the current standings in a table format
        headers = ["Joueur", "Points"]
        data = []
        # Sort players by their scores in descending order
        for player_id, score in sorted(points.items(), key=lambda x: x[1], reverse=True):
            player = Player.load_by_id(player_id)  # Load player details
            name = player.full_name() if player else player_id  # Get player name or ID
            data.append([name, score])
        print("\nClassement actuel:")
        # Print the standings table
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_message(self, msg):
        # Display an informational message
        print(f"[INFO] {msg}")
