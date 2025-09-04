import re
from rich.console import Console
from rich.table import Table
from models.player import Player

class PlayerView:
    def __init__(self, interface):
        self.console = Console()

    def display_menu(self):
        self.console.print("\n[bold magenta]--- Gestion des joueurs ---[/bold magenta]")
        self.console.print("1. Ajouter un joueur")
        self.console.print("2. Lister les joueurs")
        self.console.print("3. Modifier un joueur")
        self.console.print("4. Supprimer un joueur")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_player_data(self):
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        birth_date = input("Date de naissance (YYYY-MM-DD) : ")
        gender = input("Genre (M/F) : ")
        while True:
            national_id = input("Identifiant national d’échecs (ex: AB12345) : ").strip()
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
        return input("ID du joueur : ")

    def show_players(self, players):
        table = Table(title="Liste des joueurs")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom complet")
        table.add_column("ID National")
        for p in players:
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        self.console.print(table)

    def show_message(self, msg):
        self.console.print(f"[green]{msg}[/green]")
