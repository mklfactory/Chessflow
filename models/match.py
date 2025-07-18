class Match:
    @staticmethod
    def create_pairings(players):
        pairings = []
        for i in range(0, len(players), 2):
            p1 = players[i]
            p2 = players[i + 1] if i + 1 < len(players) else None
            pairings.append([p1, p2, 0, 0])  # Player1, Player2, score1, score2
        return pairings
