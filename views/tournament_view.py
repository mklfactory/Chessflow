class TournamentView:
    def __init__(self, interface):
        self.interface = interface

    # ---------------------------
    # Menus
    # ---------------------------
    def display_menu(self):
        print("\n--- Gestion des tournois ---")
        print("1. Ajouter un tournoi")
        print("2. Lister les tournois")
        print("3. Modifier un tournoi")
        print("4. Supprimer un tournoi")
        print("5. Gérer un tournoi (joueurs, rounds, matchs, rapports)")
        print("0. Retour")
        return input("Votre choix : ")

    def display_manage_menu(self):
        print("\n--- Gestion détaillée du tournoi ---")
        print("1. Ajouter un joueur au tournoi")
        print("2. Lister les joueurs du tournoi")
        print("3. Créer un nouveau round")
        print("4. Afficher les rounds et matchs")
        print("5. Rapports du tournoi")
        print("0. Retour")
        return input("Votre choix : ")

    # ---------------------------
    # Affichage de tournois
    # ---------------------------
    def show_tournaments(self, tournaments):
        if not tournaments:
            print("Aucun tournoi trouvé.")
        else:
            for t in tournaments:
                print(f"[{t.id}] {t.name} - {t.location} ({t.date})")

    def ask_tournament_data(self):
        return {
            "name": input("Nom du tournoi : "),
            "location": input("Lieu : "),
            "date": input("Date (YYYY-MM-DD) : "),
            "time_control": input("Contrôle du temps : "),
            "description": input("Description : "),
        }

    def ask_tournament_id(self):
        return input("ID du tournoi : ")

    # ---------------------------
    # Affichage de joueurs
    # ---------------------------
    def show_players(self, players):
        if not players:
            print("Aucun joueur inscrit dans ce tournoi.")
        else:
            for p in players:
                print(f"[{p.id}] {p.full_name()} ({p.ranking})")

    def ask_player_id(self):
        return input("ID du joueur : ")

    # ---------------------------
    # Affichage de rounds et matchs
    # ---------------------------
    def show_round_summary(self, round_obj):
        print(f"\n{round_obj.name} - Début : {round_obj.start_time or '—'} | Fin : {round_obj.end_time or '—'}")

    def show_match_detail(self, match_number, match):
        p1, p2 = match.get_players()
        p1_name = p1.full_name() if p1 else "Bye"
        p2_name = p2.full_name() if p2 else "Bye"
        print(f"  Match {match_number}: {p1_name} ({match.score1}) vs {p2_name} ({match.score2})")

    # ---------------------------
    # Messages généraux
    # ---------------------------
    def show_message(self, message):
        print(message)
