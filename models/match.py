# Modèle représentant un match entre deux joueurs
class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0.0
        self.score2 = 0.0

    def set_result(self, score1, score2):
        # Enregistre le résultat d’un match et met à jour les scores des joueurs
        self.score1 = score1
        self.score2 = score2
        self.player1.score += score1
        self.player2.score += score2

    def to_tuple(self):
        # Représentation sérialisée du match pour sauvegarde JSON
        return ([self.player1.national_id, self.score1], [self.player2.national_id, self.score2])