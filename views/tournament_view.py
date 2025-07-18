from rich.console import Console
from rich.table import Table

class TournamentView:
    def __init__(self, interface):
        self.console = interface.console

    def display_menu(self):
        self.console.print("[bold magenta]\n--- Gestion des tournois ---[/bold magenta]")
        self.console.print("1. Ajouter un tournoi")
        self.console.print("2. Lister les tournois")
        self.console.print("3. Modifier un tournoi")
        self.console.print("4. Supprimer un tournoi")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_tournament_data(self):
        name = input("Nom : ")
        location = input("Lieu : ")
        start_date = input("Date de début (YYYY-MM-DD) : ")
        end_date = input("Date de fin (YYYY-MM-DD) : ")
        description = input("Description : ")
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "players": [],
            "rounds": [],
        }

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def show_tournaments(self, tournaments):
        table = Table(title="Liste des tournois")
        table.add_column("ID")
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Date début")
        table.add_column("Date fin")
        for t in tournaments:
            table.add_row(t.id, t.name, t.location, t.start_date, t.end_date)
        self.console.print(table)

    def show_message(self, message):
        self.console.print(f"[green]{message}[/green]")
