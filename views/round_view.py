from models.player import Player
from tabulate import tabulate

class RoundView:
    def __init__(self, interface):
        pass

    def display_round_menu(self):
        print("\n--- Gestion des rounds ---")
        print("1. Créer un round manuellement")
        print("2. Voir les rounds")
        print("3. Saisir les résultats manuellement")
        print("4. Voir le classement")
        print("0. Retour")
        return input("Choisissez une option : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def show_rounds(self, rounds, tournament_name=None):
        title = "--- Gestion des rounds ---"
        if tournament_name:
            title += f" (Tournoi : {tournament_name})"
        print(title)
        headers = ["ID", "Nom", "Début", "Fin"]
        data = [[r.id, r.name, r.start_time or "", r.end_time or ""] for r in rounds]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_match(self, match, index):
        p1 = Player.load_by_id(match.player1_id)
        p2 = Player.load_by_id(match.player2_id)
        name1 = p1.full_name() if p1 else "Bye"
        name2 = p2.full_name() if p2 else "Bye"
        print(f"Match {index + 1}: {name1} vs {name2} (Scores actuels : {match.score1} - {match.score2})")

    def ask_scores(self):
        while True:
            try:
                score1 = float(input("Score joueur 1 : "))
                score2 = float(input("Score joueur 2 : "))
                if score1 < 0 or score2 < 0:
                    print("Les scores doivent être positifs.")
                    continue
                return score1, score2
            except ValueError:
                print("Entrée invalide, veuillez entrer un nombre.")

    def show_standings(self, points):
        headers = ["Joueur", "Points"]
        data = []
        for player_id, score in sorted(points.items(), key=lambda x: x[1], reverse=True):
            player = Player.load_by_id(player_id)
            name = player.full_name() if player else player_id
            data.append([name, score])
        print("\nClassement actuel :")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def show_message(self, msg):
        print(f"[INFO] {msg}")
