class TournamentView:
    def __init__(self, interface):
        # Initialize the TournamentView class
        self.interface = interface

    def display_menu(self):
        # Display the main tournament management menu
        print("\n--- Tournament Management ---")
        print("1. Add a tournament")
        print("2. List tournaments")
        print("3. Edit a tournament")
        print("4. Delete a tournament")
        print("5. Manage a tournament (players, rounds, matches, reports)")
        print("0. Back")
        # Return the user's choice
        return input("Your choice: ")

    def display_manage_menu(self):
        # Display the detailed tournament management menu
        print("\n--- Detailed Tournament Management ---")
        print("1. Add a player to the tournament")
        print("2. List players in the tournament")
        print("3. Create a new round")
        print("4. View rounds and matches")
        print("5. Tournament reports")
        print("0. Back")
        # Return the user's choice
        return input("Your choice: ")

    def show_tournaments(self, tournaments):
        # Display a list of tournaments
        if not tournaments:
            print("No tournaments found.")
        else:
            for t in tournaments:
                # Print tournament details (ID, name, location, start and end dates)
                print(f"[{t.id}] {t.name} - {t.location} ({t.start_date} - {t.end_date})")

    def ask_tournament_data(self):
        # Prompt the user to input tournament data
        return {
            "name": input("Tournament name: "),
            "location": input("Location: "),
            "start_date": input("Start date (YYYY-MM-DD): "),
            "end_date": input("End date (YYYY-MM-DD): "),
            "time_control": input("Time control: "),
            "total_rounds": int(input("Maximum number of rounds: ")),  # Input the total number of rounds
            "description": input("Description: "),
        }

    def ask_tournament_id(self):
        # Prompt the user to input a tournament ID
        return input("Tournament ID: ")

    def show_players(self, players):
        # Display a list of players in the tournament
        if not players:
            print("No players registered in this tournament.")
        else:
            for p in players:
                # Print player details (ID, full name, national ID)
                print(f"[{p.id}] {p.full_name()} ({p.national_id})")

    def ask_player_id(self):
        # Prompt the user to input a player ID
        return input("Player ID: ")

    def show_round_summary(self, round_obj):
        # Display a summary of a round (name, start time, end time)
        print(f"\n{round_obj.name} - Start: {round_obj.start_time or '—'} | End: {round_obj.end_time or '—'}")

    def show_match_detail(self, match_number, match):
        # Display details of a specific match
        p1, p2 = match.get_players()  # Get the players in the match
        p1_name = p1.full_name() if p1 else "Bye"  # Player 1 name or "Bye"
        p2_name = p2.full_name() if p2 else "Bye"  # Player 2 name or "Bye"
        # Print match details (match number, player names, and scores)
        print(f"  Match {match_number}: {p1_name} ({match.score1}) vs {p2_name} ({match.score2})")

    def show_message(self, message):
        # Display a message to the user
        print(message)
