class TournamentView:
    """
    View component for tournament management, providing console interface for tournament-related actions.
    """

    def __init__(self):
        """
        Initialize the TournamentView instance.
        """
        pass

    def display_menu(self):
        """
        Display the main tournament management menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        print("\n--- Gestion de tournoi ---")
        print("1. Ajouter un tournoi")
        print("2. Lister les tournois")
        print("3. Modifier un tournoi")
        print("4. Supprimer un tournoi")
        print("5. Gérer un tournoi (joueurs, rondes, matchs, rapports)")
        print("0. Retour")
        return input("Votre choix : ")

    def display_manage_menu(self):
        """
        Display the detailed tournament management menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        print("\n--- Gestion détaillée du tournoi ---")
        print("1. Ajouter un joueur au tournoi")
        print("2. Lister les joueurs du tournoi")
        print("3. Créer une nouvelle ronde")
        print("4. Voir les rondes et les matchs")
        print("5. Rapports de tournoi")
        print("0. Retour")
        return input("Votre choix : ")

    def show_tournaments(self, tournaments):
        """
        Display a list of tournaments.

        Args:
            tournaments (list): List of Tournament instances.
        """
        if not tournaments:
            print("Aucun tournoi trouvé.")
        else:
            for t in tournaments:
                print(f"[{t.id}] {t.name} - {t.location} ({t.start_date} - {t.end_date})")

    def ask_tournament_data(self):
        """
        Prompt the user to enter tournament data.

        Returns:
            dict: Collected tournament data.
        """
        return {
            "name": input("Nom du tournoi : "),
            "location": input("Lieu : "),
            "start_date": input("Date de début (YYYY-MM-DD) : "),
            "end_date": input("Date de fin (YYYY-MM-DD) : "),
            "time_control": input("Contrôle de temps : "),
            "total_rounds": int(input("Nombre maximum de rounds : ")),
            "description": input("Description: "),
        }

    def ask_tournament_id(self):
        """
        Prompt the user to enter a tournament ID.

        Returns:
            str: Tournament ID input by the user.
        """
        return input("ID du tournoi : ")

    def show_players(self, players):
        """
        Display a list of players registered in the tournament.

        Args:
            players (list): List of Player instances.
        """
        if not players:
            print("Aucun joueur inscrit dans ce tournoi.")
        else:
            for p in players:
                print(f"[{p.id}] {p.full_name()} ({p.national_id})")

    def ask_player_id(self):
        """
        Prompt the user to enter a player ID.

        Returns:
            str: Player ID input by the user.
        """
        return input("ID du joueur : ")

    def show_round_summary(self, round_obj):
        """
        Display a summary of a round.

        Args:
            round_obj: Round instance to display.
        """
        print(f"\n{round_obj.name} - Start: {round_obj.start_time or '—'} | End: {round_obj.end_time or '—'}")

    def show_match_detail(self, match_number, match):
        """
        Display details of a specific match.

        Args:
            match_number (int): Number/index of the match.
            match: Match instance to display.
        """
        p1, p2 = match.get_players()
        p1_name = p1.full_name() if p1 else "Bye"
        p2_name = p2.full_name() if p2 else "Bye"
        print(f"  Match {match_number}: {p1_name} ({match.score1}) vs {p2_name} ({match.score2})")

    def show_message(self, message):
        """
        Display a message to the user.

        Args:
            message (str): The message to display.
        """
        print(message)
