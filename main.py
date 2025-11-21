from controllers.main_controller import MainController

def main():
    """
    Entry point for the ChessFlow console application.
    Initializes and runs the MainController.
    """
    print("[DEBUG] Starting ChessFlow Console App...")
    app = MainController()
    app.run()

if __name__ == "__main__":
    main()
