class TournamentView:
    def __init__(self, interface):
        # Initialize the TournamentView class
        self.interface = interface

    def display_menu(self):
        # Display the main tournament management menu
        print("\n--- Gestion de tournoi ---")
        print("1. Ajouter un tournoi")
        print("2. Lister les tournois")
        print("3. Modifier un tournoi")
        print("4. Supprimer un tournoi")
        print("5. Gérer un tournoi (joueurs, rondes, matchs, rapports)")
        print("0. Retour")
        # Return the user's choice
        return input("Votre choix : ")

    def display_manage_menu(self):
        # Display the detailed tournament management menu
        print("\n--- Gestion détaillée du tournoi ---")
        print("1. Ajouter un joueur au tournoi")
        print("2. Lister les joueurs du tournoi")
        print("3. Créer une nouvelle ronde")
        print("4. Voir les rondes et les matchs")
        print("5. Rapports de tournoi")
        print("0. Retour")
        # Return the user's choice
        return input("Votre choix : ")

    def show_tournaments(self, tournaments):
        # Display a list of tournaments
        if not tournaments:
            print("Aucun tournoi trouvé.")
        else:
            for t in tournaments:
                # Print tournament details (ID, name, location, start and end dates)
                print(f"[{t.id}] {t.name} - {t.location} ({t.start_date} - {t.end_date})")

    def ask_tournament_data(self):
        # Prompt the user to input tournament data
        return {
            "name": input("Nom du tournoi : "),
            "location": input("Lieu : "),
            "start_date": input("Date de début (YYYY-MM-DD) : "),
            "end_date": input("Date de fin (YYYY-MM-DD) : "),
            "time_control": input("Contrôle de temps : "),
            "total_rounds": int(input("Nombre maximum de rounds : ")),  # Input the total number of rounds
            "description": input("Description: "),
        }

    def ask_tournament_id(self):
        # Prompt the user to input a tournament ID
        return input("ID du tournoi : ")

    def show_players(self, players):
        # Display a list of players in the tournament
        if not players:
            print("Aucun joueur inscrit dans ce tournoi.")
        else:
            for p in players:
                # Print player details (ID, full name, national ID)
                print(f"[{p.id}] {p.full_name()} ({p.national_id})")

    def ask_player_id(self):
        # Prompt the user to input a player ID
        return input("ID du joueur : ")

    def show_round_summary(self, round_obj):
        # Display a summary of a round (name, start time, end time)
        print(f"\n{round_obj.name} - Start: {round_obj.start_time or '—'} | End: {round_obj.end_time or '—'}")

    def show_match_detail(self, match_number, match):
        # Display details of a specific match
        p1, p2 = match.get_players()  # Get the players in the match
        p1_name = p1.full_name() if p1 else "Bye"  # Player 1 name or "Bye"
        p2_name = p2.full_name() if p2 else "Bye"  # Player 2 name or "Bye"
        # Print match details (match number, player names, and scores)
        print(f"  Match {match_number}: {p1_name} ({match.score1}) vs {p2_name} ({match.score2})")

    def show_message(self, message):
        # Display a message to the user
        print(message)
