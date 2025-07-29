class MainView:
    def __init__(self):
        pass

    def display_main_menu(self):
        print("\n=== ChessFlow Console App ===")
        print("1. Gérer les tournois")
        print("2. Gérer les rounds")
        print("3. Gérer les joueurs")
        print("0. Quitter")
        return input("Choisissez une option : ")
