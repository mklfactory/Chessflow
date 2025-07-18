# Entry point with CLI menu interface using rich for UI
from controllers.main_controller import MainController
from rich.console import Console

console = Console()

def main():
    controller = MainController(console)
    controller.run()

if __name__ == "__main__":
    main()
