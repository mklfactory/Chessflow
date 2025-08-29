from models.round import Round
from models.tournament import Tournament
from views.round_view import RoundView

class RoundController:
    def __init__(self, interface):
        self.view = RoundView(interface)

    def run(self):
        while True:
            choice = self.view.display_round_menu()
            if choice == "1":
                self.create_manual_round()
            elif choice == "2":
                self.view_rounds()
            elif choice == "3":
                self.update_manual_results()
            elif choice == "4":
                self.show_ranking()
            elif choice == "0":
                break

    def create_manual_round(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        round_name = input("Nom du round : ")
        match_pairs = []
        for i in range(len(tournament.players)//2):
            print(f"\nMatch {i+1}")
            p1_id = input("ID Joueur 1 : ")
            p2_id = input("ID Joueur 2 : ")
            p1 = next((p for p in tournament.players if p.id == p1_id), None)
            p2 = next((p for p in tournament.players if p.id == p2_id), None)
            match_pairs.append((p1, p2))

        round_obj = tournament.create_manual_round(round_name, match_pairs)
        self.view.show_message(f"Round '{round_obj.name}' créé avec {len(round_obj.matches)} matchs.")

    def view_rounds(self):
        rounds = Round.load_all()
        self.view.show_rounds(rounds)

    def update_manual_results(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        round_id = self.view.ask_round_id()
        round_obj = Round.load_by_id(round_id)
        if not round_obj:
            self.view.show_message("Round introuvable.")
            return

        results = []
        for i, match in enumerate(round_obj.matches):
            self.view.show_match(match, i)
            s1, s2 = self.view.ask_scores()
            results.append((s1, s2))

        tournament.update_match_results(round_obj, results)
        self.view.show_message("Résultats mis à jour et round terminé.")

    def show_ranking(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        ranking = tournament.get_ranking()
        print("\n--- Classement actuel ---")
        for i, (name, pts) in enumerate(ranking, start=1):
            print(f"{i}. {name} - {pts} points")
