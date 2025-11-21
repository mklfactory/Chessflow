from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    """
    Controller for managing players through the player view.
    Handles player creation, listing, update, and deletion.
    """

    def __init__(self):
        """
        Initialize the PlayerController and its associated view.
        """
        self.view = PlayerView()

    def run(self):
        """
        Main loop to display the player menu and handle user actions.
        """
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.add_player()
            elif choice == "2":
                self.list_players()
            elif choice == "3":
                self.update_player()
            elif choice == "4":
                self.delete_player()
            elif choice == "0":
                break
            else:
                self.view.show_message("Choix invalide.")

    def add_player(self):
        """
        Collect player data from the user, create and save a new player,
        and notify the user upon completion.
        """
        data = self.view.ask_player_data()
        player = Player(**data)
        player.save()
        self.view.show_message("Joueur ajouté.")

    def list_players(self):
        """
        Retrieve all players, sort them alphabetically,
        and display them to the user.
        """
        players = Player.load_all()
        players_sorted = Player.sort_alphabetically(players)
        self.view.show_players(players_sorted)

    def update_player(self):
        """
        Update an existing player's information.
        Asks for the player's ID, updates their attributes,
        saves changes, and notifies the user.
        """
        player_id = self.view.ask_player_id()
        player = Player.load_by_id(player_id)
        if not player:
            self.view.show_message("Joueur introuvable.")
            return
        data = self.view.ask_player_data()
        for key, value in data.items():
            setattr(player, key, value)
        player.save()
        self.view.show_message("Joueur mis à jour.")

    def delete_player(self):
        """
        Delete a player by their ID and notify the user.
        """
        player_id = self.view.ask_player_id()
        Player.delete(player_id)
        self.view.show_message("Joueur supprimé.")
