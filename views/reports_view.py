class ReportsView:
    def __init__(self, interface=None):
        # interface is ignored here because we are using print/input direct
        pass

    def display_menu(self):
        print("\n--- Rapports ---")
        print("1. Liste de tous les joueurs (alphabétique)")
        print("2. Liste de tous les tournois")
        print("3. Joueurs d’un tournoi (alphabétique)")
        print("4. Rounds et matchs d’un tournoi")
        print("0. Retour")
        return input("Votre choix : ")

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    def show_players(self, players):
        if not players:
            print("Aucun joueur trouvé.")
        else:
            for p in players:
                print(f"{p.id} - {p.full_name()} ({p.birth_date})")

    def show_tournaments(self, tournaments):
        if not tournaments:
            print("Aucun tournoi trouvé.")
        else:
            for t in tournaments:
                print(f"{t.id} - {t.name} ({t.location})")

    def show_round_summary(self, round_obj):
        print(
            f"{round_obj.name} - Début : {round_obj.start_time or '—'} | Fin : {round_obj.end_time or '—'}"
        )

    def show_match_detail(self, index, match):
        from models.player import Player
        p1 = Player.load_by_id(match.player1_id) if match.player1_id else None
        p2 = Player.load_by_id(match.player2_id) if match.player2_id else None
        name1 = p1.full_name() if p1 else "Bye"
        name2 = p2.full_name() if p2 else "Bye"
        print(f"  Match {index}: {name1} ({match.score1}) vs {name2} ({match.score2})")

    def show_message(self, message):
        print(message)
