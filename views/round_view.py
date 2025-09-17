from models.player import Player
from tabulate import tabulate


class RoundView:
    def __init__(self, interface):
        # Initialize the RoundView class
        pass

    def display_round_menu(self):
        # Display the round management menu with options
        menu = [
            ["1", "Create a round manually"],
            ["2", "View rounds"],
            ["3", "Enter results manually"],
            ["4", "View standings"],
            ["0", "Back"]
        ]
        print("\n--- Round Management ---")
        # Print the menu using the tabulate library for formatting
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        # Return the user's choice
        return input("Choose an option: ")

    def ask_round_id(self):
        # Prompt the user to input a round ID
        return input("Round ID: ")

    def show_tournament_list(self, tournaments):
        # Display a list of available tournaments in a table format
        table = [[t.id, t.name] for t in tournaments]
        print("List of available tournaments:")
        print(tabulate(table, headers=["Tournament ID", "Name"], tablefmt="fancy_grid"))

    def show_rounds(self, rounds, tournament_name=None):
        # Display a list of rounds for a tournament
        title = "--- Round Management ---"
        if tournament_name:
            # Include the tournament name in the title if provided
            title += f" (Tournament: {tournament_name})"
        print(title)
        # Define table headers and data
        headers = ["ID", "Name", "Start", "End"]
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
                score1 = float(input("Player 1 score: "))  # Input score for player 1
                score2 = float(input("Player 2 score: "))  # Input score for player 2
                if score1 < 0 or score2 < 0:
                    # Ensure scores are non-negative
                    print("Scores must be positive.")
                    continue
                return score1, score2
            except ValueError:
                # Handle invalid input
                print("Invalid input, please enter a number.")

    def show_standings(self, points):
        # Display the current standings in a table format
        headers = ["Player", "Points"]
        data = []
        # Sort players by their scores in descending order
        for player_id, score in sorted(points.items(), key=lambda x: x[1], reverse=True):
            player = Player.load_by_id(player_id)  # Load player details
            name = player.full_name() if player else player_id  # Get player name or ID
            data.append([name, score])
        print("\nCurrent standings:")
        # Print the standings table
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_message(self, msg):
        # Display an informational message
        print(f"[INFO] {msg}")
