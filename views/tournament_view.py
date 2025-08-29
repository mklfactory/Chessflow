from rich.console import Console
from rich.table import Table

class TournamentView:
    def __init__(self, interface):
        self.console = Console()

    def display_menu(self):
        self.console.print("\n[bold magenta]--- Gestion des tournois ---[/bold magenta]")
        self.console.print("1. Ajouter un tournoi")
        self.console.print("2. Lister les tournois")
        self.console.print("3. Modifier un tournoi")
        self.console.print("4. Supprimer un tournoi")
        self.console.print("5. Gérer un tournoi (joueurs, rounds, matchs, rapports)")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_tournament_data(self):
        name = input("Nom : ")
        location = input("Lieu : ")
        start_date = input("Date de début (YYYY-MM-DD) : ")
        end_date = input("Date de fin (YYYY-MM-DD) : ")
        description = input("Description : ")
        total_rounds = input("Nombre total de tours (défaut 4) : ")
        total_rounds = int(total_rounds) if str(total_rounds).isdigit() else 4
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "total_rounds": total_rounds,
            "current_round": 0,
            "rounds": [],
            "players": [],
        }

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def display_manage_menu(self):
        self.console.print("\n[bold magenta]--- Gestion détaillée du tournoi ---[/bold magenta]")
        self.console.print("1. Ajouter un joueur au tournoi")
        self.console.print("2. Lister les joueurs du tournoi")
        self.console.print("3. Créer un nouveau round")
        self.console.print("4. Afficher les rounds et matchs")
        self.console.print("5. Rapports du tournoi")
        self.console.print("0. Retour")
        return input("Votre choix : ")

    def ask_player_id(self):
        return input("ID du joueur à ajouter : ")

    def show_tournaments(self, tournaments):
        table = Table(title="Liste des tournois")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Date début")
        table.add_column("Date fin")
        for t in tournaments:
            table.add_row(t.id, t.name, t.location, t.start_date, t.end_date)
        self.console.print(table)

    def show_players(self, players):
        table = Table(title="Joueurs du tournoi")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Nom complet")
        table.add_column("ID National")
        for p in players:
            table.add_row(p.id, p.full_name(), p.national_id or "-")
        self.console.print(table)

    def show_round_summary(self, round_obj):
        self.console.print(f"[bold blue]{round_obj.name}[/bold blue] - Début : {round_obj.start_time or '—'} | Fin : {round_obj.end_time or '—'}")

    def show_match_detail(self, index, match):
        p1 = match.player1.full_name() if match.player1 else "Bye"
        p2 = match.player2.full_name() if match.player2 else "Bye"
        self.console.print(f"  • Match {index} : {p1} ({match.score1}) vs {p2} ({match.score2})")

    def show_message(self, msg):
        self.console.print(f"[green]{msg}[/green]")
