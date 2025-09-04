from tabulate import tabulate

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
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id

    def show_rounds(self, rounds, tournament_name=None):
        title = "Rounds"
        if tournament_name:
            title += f" du tournoi {tournament_name}"
        print(title)
        table = [[r.id, r.name, r.start_time or "", r.end_time or ""] for r in rounds]
        print(tabulate(table, headers=["ID", "Nom", "Début", "Fin"], tablefmt="fancy_grid"))

    def show_matches(self, matches, round_name):
        print(f"Matchs du {round_name} :")
        table = []
        for m in matches:
            table.append([m.player1_id, m.player2_id, m.score1, m.score2])
        print(tabulate(table, headers=["Joueur 1", "Joueur 2", "Score 1", "Score 2"], tablefmt="fancy_grid"))

    def show_message(self, msg):
        print(f"[INFO] {msg}")
