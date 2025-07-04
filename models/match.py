class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.data = [
            [player1, score1],
            [player2, score2]
        ]

    def to_dict(self):
        return {
            "data": [
                [p[0].to_dict(), p[1]] for p in self.data
            ]
        }

    @staticmethod
    def from_dict(data):
        from models.player import Player
        return Match(
            Player.from_dict(data["data"][0][0]),
            Player.from_dict(data["data"][1][0]),
            data["data"][0][1],
            data["data"][1][1]
        )
