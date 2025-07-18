from models.round import Round
from models.tournament import Tournament
from views.round_view import RoundView

class RoundController:
    def __init__(self, interface):
        self.view = RoundView(interface)

    def run(self):
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.create_round()
            elif choice == "2":
                self.list_rounds()
            elif choice == "3":
                self.update_match_results()
            elif choice == "4":
                self.delete_round()
            elif choice == "0":
                break

    def create_round(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        new_round = Round.create_for_tournament(tournament)
        new_round.save()
        self.view.show_message(f"Round '{new_round.name}' créé.")

    def list_rounds(self):
        rounds = Round.load_all()
        self.view.show_rounds(rounds)

    def update_match_results(self):
        round_id = self.view.ask_round_id()
        round_obj = Round.load_by_id(round_id)
        if not round_obj:
            self.view.show_message("Round introuvable.")
            return
        for idx, match in enumerate(round_obj.matches):
            self.view.show_match(match, idx)
            score1, score2 = self.view.ask_scores()
            match[2], match[3] = score1, score2
        round_obj.save()
        self.view.show_message("Résultats mis à jour.")

    def delete_round(self):
        round_id = self.view.ask_round_id()
        Round.delete(round_id)
        self.view.show_message("Round supprimé.")
