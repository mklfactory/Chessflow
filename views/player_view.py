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
        self.console.print("\n[bold magenta]--- Gestion des joueurs ---[/bold magenta]")
        self.console.print("1. Ajouter un joueur")
        self.console.print("2. Lister les joueurs")
        self.console.print("3. Modifier un joueur")
        self.console.print("4. Supprimer un joueur")
        self.console.print("0. Retour")
        # Return the user's choice
        return input("Votre choix : ")

    def ask_player_data(self):
        # Prompt the user to input player data
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        birth_date = input("Date de naissance (YYYY-MM-DD) : ")
        gender = input("Genre (M/F) : ")
        while True:
            # Validate the national chess ID format
            national_id = input("Identifiant national d’échecs (e.g., AB12345): ").strip()
            if Player.is_valid_national_id(national_id):
                break
            # Display an error message if the format is invalid
            self.console.print("[red]Format invalide. Exemple valide : AB12345[/red]")
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
        return input("ID du Joueur : ")

    def show_players(self, players):
        # Display a table of players
        table = Table(title="Liste des Joueurs")
        table.add_column("ID", style="dim", width=36)  # Column for player ID
        table.add_column("Nom Complet")                 # Column for player full name
        table.add_column("ID National")                  # Column for national chess ID
        for p in players:
            # Add a row for each player
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        # Print the table to the console
        self.console.print(table)

    def show_message(self, msg):
        # Display a message in green
        self.console.print(f"[green]{msg}[/green]")
