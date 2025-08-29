class RoundView:
    def __init__(self, interface):
        pass

    def display_round_menu(self):
        print("\n--- Gestion des rounds ---")
        print("1. Créer un round")
        print("2. Voir les rounds d'un tournoi")
        print("3. Saisir les résultats d'un round")
        print("4. Supprimer un round")
        print("0. Retour")
        return input("Choisissez une option : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def ask_round_id(self):
        return input("ID du round : ")

    def show_tournament_header(self, tournament):
        print(f"\nTournoi: {tournament.name} ({tournament.start_date} → {tournament.end_date})")

    def show_round_summary(self, round_obj):
        print(f"- {round_obj.id} | {round_obj.name} | Début: {round_obj.start_time or '—'} | Fin: {round_obj.end_time or '—'}")

    def show_match(self, match, index):
        p1 = match.player1.full_name() if match.player1 else "Bye"
        p2 = match.player2.full_name() if match.player2 else "Bye"
        print(f"Match {index+1}: {p1} vs {p2}  (scores actuels: {match.score1} - {match.score2})")

    def ask_scores(self):
        s1 = float(input("Score joueur 1 (1/0/0.5) : "))
        s2 = float(input("Score joueur 2 (1/0/0.5) : "))
        return s1, s2

    def show_message(self, msg):
        print(f"[INFO] {msg}")
