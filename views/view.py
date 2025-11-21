class View:
    """
    Basic interface view component for displaying menus and prompting user input in the console.
    """

    def main_menu(self):
        """
        Display the main menu and return the user's choice.

        Returns:
            str: User's menu selection.
        """
        print("\n--- Main Menu ---")
        print("1. Add a player")
        print("2. Create a tournament")
        print("3. View tournaments")
        print("4. Quit")
        return input("Your choice: ")

    def get_tournament_info(self):
        """
        Prompt the user to enter tournament information.

        Returns:
            tuple: Tournament data as (name, location, start, end, description).
        """
        print("\n--- Tournament Creation ---")
        name = input("Tournament name: ")
        place = input("Location: ")
        start = input("Start date: ")
        end = input("End date: ")
        description = input("Description: ")
        return name, place, start, end, description

    def get_player_info(self):
        """
        Prompt the user to enter player information.

        Returns:
            tuple: Player data as (chess_id, last, first, birth).
        """
        print("\n--- Add a Player ---")
        chess_id = input("National chess ID (e.g., AB12345): ")
        last = input("Last name: ")
        first = input("First name: ")
        birth = input("Date of birth: ")
        return chess_id, last, first, birth

    def display(self, msg):
        """
        Display a message to the user.

        Args:
            msg (str): The message to display.
        """
        print("\n" + msg)
