from models.base_model import BaseModel

class Match(BaseModel):
    def __init__(self, player1_id, player2_id, score1=0.0, score2=0.0, match_id=None):
        super().__init__(match_id)
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "score1": self.score1,
            "score2": self.score2,