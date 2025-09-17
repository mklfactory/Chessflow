class View:
    def main_menu(self):
        # Display the main menu with options
        print("\n--- Main Menu ---")
        print("1. Add a player")
        print("2. Create a tournament")
        print("3. View tournaments")
        print("4. Quit")
        # Return the user's choice
        return input("Your choice: ")

    def get_tournament_info(self):
        # Prompt the user to input tournament information
        print("\n--- Tournament Creation ---")
        name = input("Tournament name: ")  # Input the tournament name
        place = input("Location: ")        # Input the tournament location
        start = input("Start date: ")      # Input the start date
        end = input("End date: ")          # Input the end date
        description = input("Description: ")  # Input the tournament description
        # Return the collected tournament information
        return name, place, start, end, description

    def get_player_info(self):
        # Prompt the user to input player information
        print("\n--- Add a Player ---")
        chess_id = input("National chess ID (e.g., AB12345): ")  # Input the player's chess ID
        last = input("Last name: ")                              # Input the player's last name
        first = input("First name: ")                            # Input the player's first name
        birth = input("Date of birth: ")                         # Input the player's date of birth
        # Return the collected player information
        return chess_id, last, first, birth

    def display(self, msg):
        # Display a message to the user
        print("\n" + msg)
