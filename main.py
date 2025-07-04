import tkinter as tk
from controllers.controller import TournamentController

# Point d'entrée principal de l'application
# Crée une fenêtre principale et initialise le contrôleur du tournoi

def main():
    root = tk.Tk()
    root.title("ChessFlow - Centre Échecs")
    root.geometry("500x400")
    app = TournamentController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
