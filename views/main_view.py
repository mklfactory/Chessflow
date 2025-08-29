class MainView:
    def __init__(self):
        pass

    def display_main_menu(self):
        print("\n=== ChessFlow Console App ===")
        print("1. Gestion des tournois")
        print("2. Gestion des rounds")
        print("3. Gestion des joueurs")
        print("4. Rapports")
        print("0. Quitter")
        return input("Choisissez une option : ")
