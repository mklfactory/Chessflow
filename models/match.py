import uuid
import json
import os
from models.player import Player

DATA_DIR = "data"
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")

class Match:
    """
    Represents a match between two players, storing their IDs, scores, and match ID.
    Provides methods for serialization and persistent storage in a JSON file.
    """

    def __init__(self, player1_id, player2_id=None, score1=0.0, score2=0.0, id=None):
        """
        Initialize a Match instance.

        Args:
            player1_id (str): ID of the first player.
            player2_id (str, optional): ID of the second player.
            score1 (float): Score for the first player.
            score2 (float): Score for the second player.
            id (str, optional): Unique match ID. Generated if not provided.
        """
        self.id = id or str(uuid.uuid4())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def get_players(self):
        """
        Retrieve the Player instances for both players in the match.

        Returns:
            tuple: (Player instance for player 1, Player instance for player 2 or None)
        """
        p1 = Player.load_by_id(self.player1_id)
        p2 = Player.load_by_id(self.player2_id) if self.player2_id else None
        return p1, p2

    def to_dict(self):
        """
        Convert the Match instance to a dictionary for serialization.

        Returns:
            dict: Dictionary containing match attributes.
        """
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "score1": self.score1,
            "score2": self.score2,
        }

    def save(self):
        """
        Save the current match to the JSON file, updating existing if necessary.
        """
        matches = Match.load_all()
        matches = [m for m in matches if m.id != self.id]
        matches.append(self)
        Match.save_all(matches)

    @staticmethod
    def save_all(matches):
        """
        Save a list of Match instances to the JSON file.

        Args:
            matches (list): List of Match instances.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in matches], f, indent=4)

    @staticmethod
    def load_all():
        """
        Load all matches from the JSON file.

        Returns:
            list: List of Match instances.
        """
        if not os.path.exists(MATCHES_FILE):
            return []
        with open(MATCHES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Match(**m) for m in data]

    @staticmethod
    def load_by_id(match_id):
        """
        Retrieve a match by its unique ID.

        Args:
            match_id (str): Unique match ID.

        Returns:
            Match or None: Match instance if found, None otherwise.
        """
        matches = Match.load_all()
        for m in matches:
            if m.id == match_id:
                return m
        return None

    @staticmethod
    def delete_by_id(match_id):
        """
        Delete a match by its unique ID in the persistent storage.

        Args:
            match_id (str): Unique match ID to delete.
        """
        matches = Match.load_all()
        matches = [m for m in matches if m.id != match_id]
        Match.save_all(matches)
