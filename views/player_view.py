from rich.console import Console
from rich.table import Table
from models.player import Player

class PlayerView:
    """
    View component for player management, providing rich console output for user interactions.
    """

    def __init__(self):
        """
        Initialize the PlayerView and create a Console object for rich output.
        """
        self.console = Console()

    def display_menu(self):
        """
        Display the player management menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        self.console.print("\n[bold magenta]--- Gestion des joueurs ---[/bold magenta]")
        self.console.print("1. Ajouter un joueur")
        self.console.print("2. Lister les joueurs")
        self.console.print("3. Modifier un joueur")
        self.console.print("4. Supprimer un joueur")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_player_data(self):
        """
        Prompt the user for player data and validate the national ID.

        Returns:
            dict: Collected player data.
        """
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        birth_date = input("Date de naissance (YYYY-MM-DD) : ")
        gender = input("Genre (M/F) : ")
        while True:
            national_id = input("Identifiant national d’échecs (e.g., AB12345): ").strip()
            if Player.is_valid_national_id(national_id):
                break
            self.console.print("[red]Format invalide. Exemple valide : AB12345[/red]")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "gender": gender,
            "national_id": national_id,
        }

    def ask_player_id(self):
        """
        Prompt the user to input a player's ID.

        Returns:
            str: Player ID input by the user.
        """
        return input("ID du Joueur : ")

    def show_players(self, players):
        """
        Display a table listing all players.

        Args:
            players (list): List of Player instances to display.
        """
        table = Table(title="Liste des Joueurs")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom Complet")
        table.add_column("ID National")
        for p in players:
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        self.console.print(table)

    def show_message(self, msg):
        """
        Display a message in green color in the console.

        Args:
            msg (str): The message to display.
        """
        self.console.print(f"[green]{msg}[/green]")
