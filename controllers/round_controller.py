from models.round import Round
from views.round_view import RoundView
from models.tournament import Tournament

class RoundController:
    def __init__(self, interface):
        self.view = RoundView(interface)

    def run(self):
        while True:
            choice = self.view.display_round_menu()
            if choice == "1":
                self.create_round()
            elif choice == "2":
                self.view_rounds()
            elif choice == "3":
                self.update_round_results()  # Nouvelle fonctionnalité
            elif choice == "4":
                self.show_round_ranking()   # Nouvelle fonctionnalité
            elif choice == "0":
                break

    def create_round(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        round_obj = tournament.create_next_round()
        if round_obj:
            self.view.show_message(f"Round créé : {round_obj.name}")
        else:
            self.view.show_message("Tous les rounds ont déjà été créés.")

    def view_rounds(self):
        rounds = Round.load_all()
        self.view.show_rounds(rounds)

    def update_round_results(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        round_id = self.view.ask_round_id()
        round_obj = next((r for r in tournament.rounds if r.id == round_id), None)
        if not round_obj:
            self.view.show_message("Round introuvable.")
            return

        for i, match in enumerate(round_obj.matches):
            self.view.show_match(match, i)
            score1, score2 = self.view.ask_scores()
            match.score1 = score1
            match.score2 = score2

        Round.end_round(round_obj)
        tournament.save()
        self.view.show_message("Résultats mis à jour et round terminé.")

    def show_round_ranking(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        points = tournament.get_player_points()
        ranking = sorted(points.items(), key=lambda x: x[1], reverse=True)
        print("\nClassement du tournoi :")
        for i, (player_id, score) in enumerate(ranking, 1):
            player = next((p for p in tournament.players if p.id == player_id), None)
            if player:
                print(f"{i}. {player.full_name()} - {score} points")
