
   class View:
    def main_menu(self):
        print("\n--- Menu Principal ---")
        print("1. Ajouter un joueur")
        print("2. Créer un tournoi")
        print("3. Voir les tournois")
        print("4. Quitter")
        return input("Votre choix : ")

    def get_tournament_info(self):
        print("\n--- Création d'un tournoi ---")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        start = input("Date de début : ")
        end = input("Date de fin : ")
        description = input("Description : ")
        return name, place, start, end, description

    def get_player_info(self):
        print("\n--- Ajout d'un joueur ---")
        chess_id = input("Identifiant national d'échecs (ex : AB12345) : ")
        last = input("Nom : ")
        first = input("Prénom : ")
        birth = input("Date de naissance : ")
        return chess_id, last, first, birth

    def display(self, msg):
        print("\n" + msg)
