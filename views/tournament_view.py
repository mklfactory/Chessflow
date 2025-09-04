class TournamentView:
    def __init__(self, interface):
        self.interface = interface

    def display_menu(self):
        self.interface.print("\n--- Gestion des tournois ---")
        self.interface.print("1. Ajouter un tournoi")
        self.interface.print("2. Lister les tournois")
        self.interface.print("3. Modifier un tournoi")
        self.interface.print("4. Supprimer un tournoi")
        self.interface.print("5. Gérer un tournoi (joueurs, rounds, matchs, rapports)")
        self.interface.print("0. Retour")
        return self.interface.input("Votre choix : ")

    def ask_tournament_data(self):
        name = self.interface.input("Nom du tournoi : ")
        location = self.interface.input("Lieu : ")
        start_date = self.interface.input("Date de début : ")
        end_date = self.interface.input("Date de fin : ")
        description = self.interface.input("Description : ")
        total_rounds = int(self.interface.input("Nombre total de rounds : "))
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "total_rounds": total_rounds
        }

    def ask_tournament_id(self):
        return self.interface.input("ID du tournoi : ")

    def show_tournaments(self, tournaments):
        if not tournaments:
            self.interface.print("Aucun tournoi trouvé.")
        for t in tournaments:
            self.interface.print(f"{t.id} - {t.name} ({t.location}) du {t.start_date} au {t.end_date}")

    def display_manage_menu(self):
        self.interface.print("\n--- Gestion détaillée du tournoi ---")
        self.interface.print("1. Ajouter un joueur au tournoi")
        self.interface.print("2. Lister les joueurs du tournoi")
        self.interface.print("3. Créer un nouveau round")
        self.interface.print("4. Afficher les rounds et matchs")
        self.interface.print("5. Rapports du tournoi")
        self.interface.print("0. Retour")
        return self.interface.input("Votre choix : ")

    def ask_player_id(self):
        return self.interface.input("ID du joueur : ")

    def show_players(self, players):
        if not players:
            self.interface.print("Aucun joueur trouvé.")
        for p in players:
            self.interface.print(f"{p.id} - {p.full_name()} ({p.birth_date})")

    def show_round_summary(self, round_obj):
        self.interface.print(
            f"{round_obj.name} - Début : {round_obj.start_date or '—'} | Fin : {round_obj.end_date or '—'}"
        )

    def show_match_detail(self, index, match):
        from models.player import Player
        p1 = Player.load_by_id(match.player1_id) if match.player1_id else None
        p2 = Player.load_by_id(match.player2_id) if match.player2_id else None
        name1 = p1.full_name() if p1 else "Bye"
        name2 = p2.full_name() if p2 else "Bye"
        self.interface.print(f"  Match {index}: {name1} ({match.score1}) vs {name2} ({match.score2})")

    def show_message(self, message):
        self.interface.print(message)
