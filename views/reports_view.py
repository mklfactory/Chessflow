from tabulate import tabulate
from models.player import Player
class ReportView:
    def __init__(self, interface):
        pass

    def display_report_menu(self):
        menu = [
            ["1", "Liste de tous les joueurs (alphabétique)"],
            ["2", "Liste de tous les tournois"],
            ["3", "Joueurs d’un tournoi (alphabétique)"],
            ["4", "Rounds et matchs d’un tournoi"],
            ["0", "Retour"]
        ]
        print("\n--- Rapports ---")
        print(tabulate(menu, headers=["Option", "Description"], tablefmt="fancy_grid"))
        return input("Votre choix : ")

    def show_players_list(self, players):
        table = [[p.id, f"{p.last_name} {p.first_name}", p.birth_date] for p in players]
        print("Liste des joueurs :")
        print(tabulate(table, headers=["ID", "Nom", "Date de naissance"], tablefmt="fancy_grid"))

    def show_tournament_list(self, tournaments):
        table = [[t.id, t.name] for t in tournaments]
        print("Liste des tournois :")
        print(tabulate(table, headers=["ID", "Nom"], tablefmt="fancy_grid"))

    def ask_tournament_selection(self):
        tournament_id = input("ID du tournoi : ")
        return tournament_id

    def show_rounds_and_matches(self, rounds, tournament_name=None):
        print(f"\nRounds et matchs du tournoi : {tournament_name}")
        for r in rounds:
            print(f"\n{r.name} - Début : {r.start_time or '—'} | Fin : {r.end_time or '—'}")
            table = []
            for i, match in enumerate(r.matches, 1):
                p1 = Player.load_by_id(match.player1_id)
                p2 = Player.load_by_id(match.player2_id)
                name1 = p1.full_name() if p1 else "Bye"
                name2 = p2.full_name() if p2 else "Bye"
                table.append([f"Match {i}", f"{name1} ({match.score1})", f"{name2} ({match.score2})"])
            print(tabulate(table, headers=["Match", "Joueur 1 (Score)", "Joueur 2 (Score)"], tablefmt="fancy_grid"))

    def show_message(self, msg):
        print(f"[INFO] {msg}")
