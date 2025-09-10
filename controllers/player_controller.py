# Importing the Player model and the PlayerView for managing players
from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    def __init__(self, interface):
        # Initialize the PlayerView with the main interface
        self.view = PlayerView(interface)

    def run(self):
        # Main loop for managing players
        while True:
            # Display the player menu and get the user's choice
            choice = self.view.display_menu()
            if choice == "1":
                self.add_player()  # Add a new player
            elif choice == "2":
                self.list_players()  # List all players
            elif choice == "3":
                self.update_player()  # Update an existing player
            elif choice == "4":
                self.delete_player()  # Delete a player
            elif choice == "0":
                # Exit the player management menu
                break
            else:
                # Handle invalid input
                self.view.show_message("Choix invalide.")

    def add_player(self):
        # Collect player data from the user
        data = self.view.ask_player_data()
        # Create a new Player instance with the provided data
        player = Player(**data)
        # Save the player to the database or storage
        player.save()
        # Notify the user that the player was added
        self.view.show_message("Joueur ajouté.")

    def list_players(self):
        # Load all players from the database or storage
        players = Player.load_all()
        # Sort players alphabetically
        players_sorted = Player.sort_alphabetically(players)
        # Display the sorted list of players
        self.view.show_players(players_sorted)

    def update_player(self):
        # Ask the user for the ID of the player to update
        player_id = self.view.ask_player_id()
        # Load the player by ID
        player = Player.load_by_id(player_id)
        if not player:
            # Notify the user if the player is not found
            self.view.show_message("Joueur introuvable.")
            return
        # Collect updated player data from the user
        data = self.view.ask_player_data()
        # Update the player's attributes with the new data
        for key, value in data.items():
            setattr(player, key, value)
        # Save the updated player to the database or storage
        player.save()
        # Notify the user that the player was updated
        self.view.show_message("Joueur mis à jour.")

    def delete_player(self):
        # Ask the user for the ID of the player to delete
        player_id = self.view.ask_player_id()
        # Delete the player from the database or storage
        Player.delete(player_id)
        # Notify the user that the player was deleted
        self.view.show_message("Joueur supprimé.")
