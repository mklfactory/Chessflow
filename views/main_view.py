class MainView:
    def __init__(self):
        # Constructor for the MainView class
        pass

    def display_main_menu(self):
        # Displays the main menu of the ChessFlow console application
        print("\n=== ChessFlow Console App ===")  # Title of the application
        print("1. Gestion des tournois")        # Option 1: Tournament management
        print("2. Gestion des rounds")          # Option 2: Round management
        print("3. Gestion des joueurs")         # Option 3: Player management
        print("4. Rapports")                    # Option 4: Reports
        print("0. Quitter")                     # Option 0: Exit the application
        return input("Choisissez une option : ") # Prompt the user to choose
