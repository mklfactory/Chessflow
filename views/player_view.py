from rich.console import Console
from rich.table import Table
from models.player import Player


class PlayerView:
    def __init__(self, interface):
        # Initialize the PlayerView class
        # Create a Console object for rich text output
        self.console = Console()

    def display_menu(self):
        # Display the player management menu
        self.console.print("\n[bold magenta]--- Player Management ---[/bold magenta]")
        self.console.print("1. Add a player")
        self.console.print("2. List players")
        self.console.print("3. Edit a player")
        self.console.print("4. Delete a player")
        self.console.print("0. Back")
        # Return the user's choice
        return input("Your choice: ")

    def ask_player_data(self):
        # Prompt the user to input player data
        first_name = input("First name: ")
        last_name = input("Last name: ")
        birth_date = input("Date of birth (YYYY-MM-DD): ")
        gender = input("Gender (M/F): ")
        while True:
            # Validate the national chess ID format
            national_id = input("National chess ID (e.g., AB12345): ").strip()
            if Player.is_valid_national_id(national_id):
                break
            # Display an error message if the format is invalid
            self.console.print("[red]Invalid format. Valid example: AB12345[/red]")
        # Return the collected player data as a dictionary
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "gender": gender,
            "national_id": national_id,
        }

    def ask_player_id(self):
        # Prompt the user to input a player's ID
        return input("Player ID: ")

    def show_players(self, players):
        # Display a table of players
        table = Table(title="Player List")
        table.add_column("ID", style="dim", width=36)  # Column for player ID
        table.add_column("Full Name")                 # Column for player full name
        table.add_column("National ID")               # Column for national chess ID
        for p in players:
            # Add a row for each player
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        # Print the table to the console
        self.console.print(table)

    def show_message(self, msg):
        # Display a message in green
        self.console.print(f"[green]{msg}[/green]")
