class Match:
    def __init__(self, player1=None, player2=None, score1=0.0, score2=0.0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = float(score1)
        self.score2 = float(score2)

    def to_list(self):
        return [[self.player1.id if self.player1 else None, self.score1],
                [self.player2.id if self.player2 else None, self.score2]]

    @staticmethod
    def from_list(data):
        # data: [[player1_id, score1], [player2_id, score2]]
        from models.player import Player
        p1 = Player.load_by_id(data[0][0]) if data[0][0] else None
        p2 = Player.load_by_id(data[1][0]) if data[1][0] else None
        s1 = float(data[0][1])
        s2 = float(data[1][1])
        return Match(p1, p2, s1, s2)
