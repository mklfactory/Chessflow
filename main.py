from controllers.main_controller import MainController

def main():
    print("[DEBUG] Starting ChessFlow Console App...")
    app = MainController()
    app.run()

if __name__ == "__main__":
    main()