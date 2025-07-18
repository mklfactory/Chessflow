from rich.console import Console
from rich.table import Table

class PlayerView:
    def __init__(self, interface):
        self.console = interface.console

    def display_menu(self):
        self.console.print("[bold cyan]\n--- Gestion des joueurs ---[/bold cyan]")
        self.console.print("1. Ajouter un joueur")
        self.console.print("2. Lister les joueurs")
        self.console.print("3. Modifier un joueur")
        self.console.print("4. Supprimer un joueur")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_player_data(self):
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        birthdate = input("Date de naissance (YYYY-MM-DD) : ")
        ranking = int(input("Classement : "))
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "ranking": ranking,
        }

    def ask_player_id(self):
        return input("ID du joueur : ")

    def show_players(self, players):
        table = Table(title="Liste des joueurs")
        table.add_column("ID")
        table.add_column("Prénom")
        table.add_column("Nom")
        table.add_column("Date de naissance")
        table.add_column("Classement")
        for p in players:
            table.add_row(p.id, p.first_name, p.last_name, p.birthdate, str(p.ranking))
        self.console.print(table)

    def show_message(self, message):
        self.console.print(f"[green]{message}[/green]")
