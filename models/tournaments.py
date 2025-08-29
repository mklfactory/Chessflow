def create_manual_round(self, round_name, match_pairs):
    """
    Crée un round avec des matchs définis manuellement.
    match_pairs = [(player1, player2), ...]
    """
    from models.round import Round
    from models.match import Match
    matches = [Match(p1, p2) for p1, p2 in match_pairs]
    new_round = Round(name=round_name, matches=matches)
    Round.start_round(new_round)
    self.rounds.append(new_round)
    self.current_round += 1
    new_round.save()
    self.save()
    return new_round

def update_match_results(self, round_obj, results):
    """
    Met à jour les scores des matchs du round.
    results = [(score1, score2), ...] dans le même ordre que round_obj.matches
    """
    for match, (s1, s2) in zip(round_obj.matches, results):
        match.score1 = s1
        match.score2 = s2
    from models.round import Round
    Round.end_round(round_obj)
    round_obj.save()
    self.save()

def get_ranking(self):
    """
    Retourne un classement des joueurs basé sur les points cumulés.
    """
    points = self.get_player_points()
    ranking = sorted(self.players, key=lambda p: points[p.id], reverse=True)
    return [(p.full_name(), points[p.id]) for p in ranking]
