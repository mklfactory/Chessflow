# Importing the MainController class from the controllers.main_controller module
from controllers.main_controller import MainController

# The main function serves as the entry point for the application


def main():
    # Debug message to indicate the application is starting
    print("[DEBUG] Starting ChessFlow Console App...")
    # Creating an instance of the MainController class
    app = MainController()
    # Calling the run method of the MainController instance to start the application
    app.run()

# This ensures the main function is executed only when the script is run directly,
# and not when it is imported as a module in another script

if __name__ == "__main__":
    main()
    