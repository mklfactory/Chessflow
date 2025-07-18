from rich.console import Console

class MainView:
    def __init__(self):
        self.console = Console()

    def display_main_menu(self):
        self.console.print("[bold blue]=== Menu Principal ===[/bold blue]")
        self.console.print("1. Gestion des tournois")
        self.console.print("2. Gestion des rounds")
        self.console.print("3. Gestion des joueurs")
        self.console.print("0. Quitter")
        return input("Choisissez une option : ")
