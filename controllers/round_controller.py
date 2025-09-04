from models.tournament import Tournament
from views.round_view import RoundView
from datetime import datetime

class RoundController:
    def __init__(self, interface):
        self.view = RoundView(interface)

    def ask_tournament_selection(self):
        tournaments = Tournament.load_all()
        print("Liste des tournois disponibles :")
        for t in tournaments:
            print(f"{t.id} - {t.name}")
        tournament_id = input("Sélectionnez l'ID du tournoi : ")
        return tournament_id

    def run(self):
        while True:
            choice = self.view.display_round_menu()
            if choice == "1":
                self.create_manual_round()
            elif choice == "2":
                self.show_rounds()
            elif choice == "3":
                self.enter_results_manually()
            elif choice == "4":
                self.show_standings()
            elif choice == "0":
                break

    def create_manual_round(self):
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return

        if tournament.current_round >= tournament.total_rounds:
            self.view.show_message("Tous les rounds ont déjà été créés.")
            return

        round_obj = tournament.create_next_round()
        if round_obj:
            round_obj.save()
            tournament.save()
            self.view.show_message(f"Nouveau round créé : {round_obj.name}")
        else:
            self.view.show_message("Impossible de créer un nouveau round.")

    def show_rounds(self):
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        self.view.show_rounds(tournament.rounds, tournament.name)

    def enter_results_manually(self):
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        if not tournament.rounds:
            self.view.show_message("Aucun round dans ce tournoi.")
            return

        self.view.show_rounds(tournament.rounds, tournament.name)
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
            match.save()

        round_obj.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        round_obj.save()
        self.view.show_message(f"Résultats du {round_obj.name} mis à jour.")

    def show_standings(self):
        tournament_id = self.ask_tournament_selection()
        tournament = Tournament.load_by_id(tournament_id)
        if not tournament:
            self.view.show_message("Tournoi introuvable.")
            return
        points = self.calculate_points(tournament)
        self.view.show_standings(points)

    def calculate_points(self, tournament):
        points = {pid: 0.0 for pid in tournament.player_ids}
        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                points[match.player1_id] += match.score1
                points[match.player2_id] += match.score2
        return points
