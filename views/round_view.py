from rich.console import Console
from rich.table import Table

class RoundView:
    def __init__(self, interface):
        self.console = Console()

    def display_round_menu(self):
        self.console.print("\n[bold magenta]--- Gestion des rounds ---[/bold magenta]")
        self.console.print("1. Créer un round")
        self.console.print("2. Voir les rounds")
        self.console.print("3. Mettre à jour les résultats d'un match")
        self.console.print("4. Supprimer un round")
        self.console.print("0. Retour")
        return input("Choisissez une option : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def show_rounds(self, rounds):
        table = Table(title="Liste des rounds")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom")
        table.add_column("Début")
        table.add_column("Fin")
        for r in rounds:
            table.add_row(r.id, r.name, str(r.start_time or "non démarré"), str(r.end_time or "non terminé"))
        self.console.print(table)

    def show_match(self, match, index):
        p1 = match.player1.full_name() if match.player1 else "Bye"
        p2 = match.player2.full_name() if match.player2 else "Bye"
        self.console.print(f"Match {index+1}: {p1} vs {p2} (Scores actuels : {match.score1} - {match.score2})")

    def ask_scores(self):
        score1 = float(input("Score joueur 1 : "))
        score2 = float(input("Score joueur 2 : "))
        return score1, score2

    def show_message(self, msg):
        self.console.print(f"[green]{msg}[/green]")
