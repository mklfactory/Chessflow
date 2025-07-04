# Contrôleur principal qui gère l'interface utilisateur et la logique
import tkinter as tk
from tkinter import messagebox
from models.player import Player
from models.tournament import Tournament
from models.round import Round

class TournamentController:
    def __init__(self, root):
        self.root = root
        self.players = []
        self.tournaments = []
        self.menu()

    def menu(self):
        # Affiche le menu principal avec des boutons
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="1. Ajouter un joueur", command=self.add_player).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="2. Créer un tournoi", command=self.create_tournament).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="3. Lancer un tour", command=self.launch_round).pack(fill="x", padx=50, pady=5)
        tk.Button(self.root, text="4. Quitter", command=self.root.quit).pack(fill="x", padx=50, pady=5)

    def add_player(self):
        # Ouvre un formulaire pour ajouter un joueur
        self._open_form("Ajout Joueur", self._add_player_callback, ["ID national", "Nom", "Prénom", "Date naissance"])

    def _add_player_callback(self, entries):
        # Callback qui ajoute un joueur à la liste
        pid, last, first, dob = entries
        player = Player(pid, last, first, dob)
        self.players.append(player)
        messagebox.showinfo("Succès", f"Joueur {first} {last} ajouté !")
        self.menu()

    def create_tournament(self):
        # Ouvre un formulaire pour créer un tournoi
        self._open_form("Créer Tournoi", self._create_tournament_callback,
                        ["Nom", "Lieu", "Date début", "Date fin", "Description"])

    def _create_tournament_callback(self, entries):
        # Callback qui crée un tournoi et y ajoute les joueurs existants
        name, place, start, end, description = entries
        t = Tournament(name, place, start, end, description)
        for p in self.players:
            t.add_player(p)
        self.tournaments.append(t)
        messagebox.showinfo("Succès", f"Tournoi '{name}' créé avec {len(t.players)} joueurs !")
        self.menu()

    def launch_round(self):
        # Lance un nouveau tour pour le tournoi en cours
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
        r.end_round()  # On suppose les matchs joués directement ici pour simplifier
        current_tournament.add_round(r)

        messagebox.showinfo("Tour joué", f"{r_name} joué avec {len(r.matches)} matchs.")
        self.menu()

    def _open_form(self, title, callback, labels):
        # Ouvre une fenêtre de formulaire avec plusieurs champs texte
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
        # Vérifie les entrées et appelle la fonction callback correspondante
        values = [e.get().strip() for e in entries]
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        form.destroy()
        callback(values)