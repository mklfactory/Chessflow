from models.player import Player

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

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def show_rounds(self, rounds):
        for r in rounds:
            print(f"{r.id} - {r.name} - Début: {r.start_time} - Fin: {r.end_time}")

    def show_match(self, match, index):
        p1, p2 = match.get_players()
        p1_name = p1.full_name() if p1 else "Bye"
        p2_name = p2.full_name() if p2 else "Bye"
        print(f"Match {index+1}: {p1_name} vs {p2_name} (Scores actuels : {match.score1} - {match.score2})")

    def ask_scores(self):
        score1 = float(input("Score joueur 1 : "))
        score2 = float(input("Score joueur 2 : "))
        return score1, score2

    def show_standings(self, points):
        print("\nClassement actuel :")
        sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
        for player_id, score in sorted_points:
            player = Player.load_by_id(player_id)
            if player:
                print(f"{player.full_name()} : {score} points")
            else:
                print(f"{player_id} : {score} points (joueur introuvable)")

    def show_message(self, msg):
        print(f"[INFO] {msg}")
