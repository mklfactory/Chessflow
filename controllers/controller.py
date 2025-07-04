import tkinter as tk
from tkinter import messagebox
import json
import os
from models.player import Player
from models.tournament import Tournament
from models.round import Round

class TournamentController:
    def __init__(self, root):
        self.root = root
        self.players = self.load_players()
        self.tournaments = self.load_tournaments()
        self.menu()

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="1. Ajouter un joueur", command=self.add_player).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="2. Créer un tournoi", command=self.create_tournament).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="3. Lancer un tour", command=self.launch_round).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="4. Quitter", command=self.save_and_exit).pack(fill="x", padx=50, pady=5)

    def add_player(self):
        self._open_form("Ajout Joueur", self._add_player_callback, ["ID national", "Nom", "Prénom", "Date naissance"])

    def _add_player_callback(self, entries):
        pid, last, first, dob = entries
        player = Player(pid, last, first, dob)
        self.players.append(player)
        messagebox.showinfo("Succès", f"Joueur {first} {last} ajouté !")
        self.menu()

    def create_tournament(self):
        self._open_form("Créer Tournoi", self._create_tournament_callback,
                        ["Nom", "Lieu", "Date début", "Date fin", "Description"])

    def _create_tournament_callback(self, entries):
        name, place, start, end, description = entries
        t = Tournament(name, place, start, end, description)
        for p in self.players:
            t.add_player(p)
        self.tournaments.append(t)
        messagebox.showinfo("Succès", f"Tournoi '{name}' créé avec {len(t.players)} joueurs !")
        self.menu()

    def launch_round(self):
        if not self.tournaments:
            messagebox.showwarning("Aucun tournoi", "Veuillez d'abord créer un tournoi.")
            return

        current_tournament = self.tournaments[-1]
        if current_tournament.current_round >= current_tournament.rounds:
            messagebox.showinfo("Tournoi terminé", "Tous les tours ont déjà été joués.")
            return

        r_name = f"Round {current_tournament.current_round + 1}"
        r = Round(r_name)
        r.generate_matches(current_tournament.players)

        for match in r.matches:
            result = self._ask_score(match)
            if result:
                score1, score2 = result
                match.set_result(score1, score2)

        r.end_round()
        current_tournament.add_round(r)

        messagebox.showinfo("Tour joué", f"{r_name} joué avec {len(r.matches)} matchs.")
        self.menu()

    def _ask_score(self, match):
        dialog = tk.Toplevel(self.root)
        dialog.title("Saisir le résultat")
        tk.Label(dialog, text=f"{match.player1.first_name} vs {match.player2.first_name}").pack()

        entry1 = tk.Entry(dialog)
        entry1.insert(0, "0.0")
        entry1.pack()
        entry2 = tk.Entry(dialog)
        entry2.insert(0, "0.0")
        entry2.pack()

        result = []

        def submit():
            try:
                s1 = float(entry1.get())
                s2 = float(entry2.get())
                result.extend([s1, s2])
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Scores invalides")

        tk.Button(dialog, text="Valider", command=submit).pack(pady=10)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result if result else None

    def _open_form(self, title, callback, labels):
        form = tk.Toplevel(self.root)
        form.title(title)
        entries = []
        for label in labels:
            tk.Label(form, text=label).pack()
            entry = tk.Entry(form)
            entry.pack()
            entries.append(entry)
        tk.Button(form, text="Valider", command=lambda: self._submit_form(form, entries, callback)).pack(pady=10)

    def _submit_form(self, form, entries, callback):
        values = [e.get().strip() for e in entries]
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        form.destroy()
        callback(values)

    def save_and_exit(self):
        self.save_players()
        self.save_tournaments()
        self.root.quit()

    def save_players(self):
        os.makedirs("data", exist_ok=True)
        with open("data/players.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.players], f, indent=2)

    def load_players(self):
        try:
            with open("data/players.json", "r", encoding="utf-8") as f:
                return [Player.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            return []

    def save_tournaments(self):
        os.makedirs("data", exist_ok=True)
        with open("data/tournaments.json", "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tournaments], f, indent=2)

    def load_tournaments(self):
        try:
            with open("data/tournaments.json", "r", encoding="utf-8") as f:
                return [Tournament.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            return []
