# Modèle représentant un joueur d'échecs
class Player:
    def __init__(self, national_id, last_name, first_name, birth_date):
        self.national_id = national_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.score = 0

    def to_dict(self):
        # Convertit un joueur en dictionnaire (pour sauvegarde JSON)
        return {
            "national_id": self.national_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "score": self.score,
        }

    @staticmethod
    def from_dict(data):
        # Crée un joueur à partir d'un dictionnaire
        player = Player(
            data["national_id"],
            data["last_name"],
            data["first_name"],
            data["birth_date"]
        )
        player.score = data.get("score", 0)
        return player
