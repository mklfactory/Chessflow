from tabulate import tabulate
from models.player import Player


class ReportView:
    def __init__(self, interface):
        # Initialize the ReportView class
        pass

    def display_report_menu(self):
        # Display the report menu with options
        menu = [
            ["1", "List of all players (alphabetical)"],
            ["2", "List of all tournaments"],
            ["3", "Players of a tournament (alphabetical)"],
            ["4", "Rounds and matches of a tournament"],
            ["0", "Back"]
        ]
        print("\n--- Reports ---")
        # Print the menu using the tabulate library for formatting
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        # Return the user's choice
        return input("Your choice: ")

    def show_players_list(self, players):
        # Display a list of players in a table format
        table = [[p.id, f"{p.last_name} {p.first_name}", p.birth_date] for p in players]
        print("List of players:")
        print(tabulate(table, headers=["ID", "Name", "Date of Birth"], tablefmt="fancy_grid"))

    def show_tournament_list(self, tournaments):
        # Display a list of tournaments in a table format
        table = [[t.id, t.name] for t in tournaments]
        print("List of tournaments:")
        print(tabulate(table, headers=["ID", "Name"], tablefmt="fancy_grid"))

    def ask_tournament_selection(self):
        # Prompt the user to input a tournament ID
        tournament_id = input("Tournament ID: ")
        return tournament_id

    def show_rounds_and_matches(self, rounds, tournament_name=None):
        # Display the rounds and matches of a tournament
        print(f"\nRounds and matches of the tournament: {tournament_name}")
        for r in rounds:
            # Display round details (name, start time, end time)
            print(f"\n{r.name} - Start: {r.start_time or '—'} | End: {r.end_time or '—'}")
            table = []
            for i, match in enumerate(r.matches, 1):
                # Load player details for each match
                p1 = Player.load_by_id(match.player1_id)
                p2 = Player.load_by_id(match.player2_id)
                name1 = p1.full_name() if p1 else "Bye"  # Player 1 name or "Bye"
                name2 = p2.full_name() if p2 else "Bye"  # Player 2 name or "Bye"
                # Add match details to the table
                table.append([f"Match {i}", f"{name1} ({match.score1})", f"{name2} ({match.score2})"])
            # Print the table of matches
            print(tabulate(table, headers=["Match", "Player 1 (Score)", "Player 2 (Score)"], tablefmt="fancy_grid"))

    def show_message(self, msg):
        # Display an informational message
        print(f"[INFO] {msg}")
