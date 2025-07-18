from rich.console import Console
from rich.table import Table

class RoundView:
    def __init__(self, interface):
        self.console = interface.console

    def display_menu(self):
        self.console.print("[bold yellow]\n--- Gestion des rounds ---[/bold yellow]")
        self.console.print("1. Créer un round")
        self.console.print("2. Afficher les rounds")
        self.console.print("3. Modifier les résultats d'un match")
        self.console.print("4. Supprimer un round")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def ask_scores(self):
        s1 = float(input("Score joueur 1 : "))
        s2 = float(input("Score joueur 2 : "))
        return s1, s2

    def show_rounds(self, rounds):
        table = Table(title="Rounds")
        table.add_column("ID")
        table.add_column("Nom")
        for r in rounds:
            table.add_row(r.id, r.name)
        self.console.print(table)

    def show_match(self, match, index):
        self.console.print(f"[yellow]Match {index + 1}: {match[0]} vs {match[1]}[/yellow]")

    def show_message(self, message):
        self.console.print(f"[green]{message}[/green]")
