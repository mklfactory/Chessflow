from views.round_view import RoundView
from models.tournament import Tournament
from models.round import Round

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
                self.update_match_result()
            elif choice == "4":
                self.delete_round()
            elif choice == "0":
                break
            else:
                self.view.show_message("Choix invalide.")

    def _get_tournament_or_msg(self):
        tournament_id = self.view.ask_tournament_id()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return None
        return tournament

    def create_round(self):
        tournament = self._get_tournament_or_msg()
        if not tournament:
            return
        round_obj = tournament.create_next_round()
        if round_obj:
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
        else:
            self.view.show_message("Tous les rounds ont déjà été créés.")

    def view_rounds(self):
        tournament = self._get_tournament_or_msg()
        if not tournament:
            return
        self.view.show_tournament_header(tournament)
        for r in tournament.rounds:
            self.view.show_round_summary(r)

    def update_match_result(self):
        tournament = self._get_tournament_or_msg()
        if not tournament:
            return

        round_id = self.view.ask_round_id()
        round_obj = next((r for r in tournament.rounds if r.id == round_id), None)
        if not round_obj:
            self.view.show_message("Round introuvable.")
            return

        for i, match in enumerate(round_obj.matches):
            self.view.show_match(match, i)
            score1, score2 = self.view.ask_scores()
            # règles de points : 1/0 ou 0.5/0.5
            if score1 not in (0, 0.5, 1) or score2 not in (0, 0.5, 1) or (score1 + score2) not in (1, 1.0):
                self.view.show_message("Scores invalides. Utilisez (1,0), (0,1) ou (0.5,0.5).")
                return
            match.score1 = float(score1)
            match.score2 = float(score2)

        Round.end_round(round_obj)
        tournament.save()
        self.view.show_message("Résultats enregistrés. Round terminé.")

    def delete_round(self):
        tournament = self._get_tournament_or_msg()
        if not tournament:
            return
        round_id = self.view.ask_round_id()
        before = len(tournament.rounds)
        tournament.rounds = [r for r in tournament.rounds if r.id != round_id]
        if len(tournament.rounds) < before:
            tournament.save()
            self.view.show_message("Round supprimé.")
        else:
            self.view.show_message("Round introuvable.")
