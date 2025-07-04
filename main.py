import tkinter as tk
from controllers.controller import TournamentController

def main():
    root = tk.Tk()
    root.title("ChessFlow - Centre Échecs")
    root.geometry("500x400")
    app = TournamentController(root)
    root.mainloop()

if __name__ == "__main__":
    main()