from rich.console import Console
from rich.table import Table

class ReportsView:
    def __init__(self, interface):
        self.console = Console()

    def display_menu(self):
        self.console.print("\n[bold yellow]--- Rapports ---[/bold yellow]")
        self.console.print("1. Liste de tous les joueurs (A→Z)")
        self.console.print("2. Liste de tous les tournois")
        self.console.print("3. Infos d’un tournoi (nom & dates)")
        self.console.print("4. Joueurs d’un tournoi (A→Z)")
        self.console.print("5. Rounds & matchs d’un tournoi")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def show_players(self, players):
        table = Table(title="Joueurs")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom complet")
        table.add_column("ID National")
        for p in players:
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        self.console.print(table)

    def show_tournaments(self, tournaments):
        table = Table(title="Tournois")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Début")
        table.add_column("Fin")
        for t in tournaments:
            table.add_row(t.id, t.name, t.location, t.start_date, t.end_date)
        self.console.print(table)

    def show_tournament_info(self, t):
        self.console.print(f"[bold]Tournoi[/bold] : {t.name}")
        self.console.print(f"Lieu : {t.location}")
        self.console.print(f"Dates : {t.start_date} → {t.end_date}")
        self.console.print(f"Tours : {t.current_round}/{t.total_rounds}")
        self.console.print(f"Description : {t.description or '—'}")

    def show_round_summary(self, round_obj):
        self.console.print(f"[bold blue]{round_obj.name}[/bold blue] - Début : {round_obj.start_time or '—'} | Fin : {round_obj.end_time or '—'}")

    def show_match_detail(self, index, match):
        p1 = match.player1.full_name() if match.player1 else "Bye"
        p2 = match.player2.full_name() if match.player2 else "Bye"
        self.console.print(f"  • Match {index} : {p1} ({match.score1}) vs {p2} ({match.score2})")

    def show_message(self, msg):
        self.console.print(f"[green]{msg}[/green]")
