from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class MainController:
    def __init__(self, console):
        self.console = console

    def run(self):
        while True:
            self.console.print(Panel("[bold cyan]=== ChessFlow Menu ===[/bold cyan]", expand=False))
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Option", justify="center")
            table.add_column("Action", justify="left")
            table.add_row("1", "Add Player")
            table.add_row("2", "Create Tournament")
            table.add_row("3", "Play Round")
            table.add_row("4", "Quit")
            self.console.print(table)

            choice = input("Choose an option: ")

            if choice == "1":
                PlayerController().add_player()
            elif choice == "2":
                TournamentController().create_tournament()
            elif choice == "3":
                RoundController().play_round()
            elif choice == "4":
                self.console.print("[bold red]Exiting ChessFlow.[/bold red]")
                break
            else:
                self.console.print("[red]Invalid choice. Try again.[/red]")
