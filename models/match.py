class Match:
    def __init__(self, player1=None, player2=None, score1=0, score2=0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_list(self):
        return [[self.player1.id if self.player1 else None, self.score1],
                [self.player2.id if self.player2 else None, self.score2]]

    @staticmethod
    def from_list(data):
        # Data example: [[player1_id, score1], [player2_id, score2]]
        from models.player import Player
        player1 = Player.load_by_id(data[0][0]) if data[0][0] else None
        player2 = Player.load_by_id(data[1][0]) if data[1][0] else None
        return Match(player1, player2, data[0][1], data[1][1])

    @staticmethod
    def create_pairings(players):
        pairings = []
        for i in range(0, len(players), 2):
            p1 = players[i]
            p2 = players[i+1] if i+1 < len(players) else None
            pairings.append(Match(p1, p2))
        return pairings
