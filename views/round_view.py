from models.match import Match

class RoundView:
    def __init__(self, interface):
        pass

    def display_round_menu(self):
        print("\n--- Gestion des rounds ---")
        print("1. Créer un round")
        print("2. Voir les rounds")
        print("3. Mettre à jour les résultats d'un round")  # Nouvelle option
        print("4. Voir le classement")  # Nouvelle option
        print("0. Retour")
        return input("Choisissez une option : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def show_rounds(self, rounds):
        for r in rounds:
            print(f"{r.id} - {r.name} - Début: {r.start_time or 'non démarré'} - Fin: {r.end_time or 'non terminé'}")

    def show_match(self, match, index):
        p1 = match.player1.full_name() if match.player1 else "Bye"
        p2 = match.player2.full_name() if match.player2 else "Bye"
        print(f"Match {index+1}: {p1} vs {p2} (Scores actuels : {match.score1} - {match.score2})")

    def ask_scores(self):
        score1 = float(input("Score joueur 1 : "))
        score2 = float(input("Score joueur 2 : "))
        return score1, score2

    def show_message(self, msg):
        print(f"[INFO] {msg}")
