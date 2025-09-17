import uuid
import json
import os
from models.player import Player

# Directory and file path for storing match data
DATA_DIR = "data"
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")


class Match:
    def __init__(self, player1_id, player2_id=None, score1=0.0, score2=0.0, id=None):
        # Initialize a Match object with player IDs, scores, and a unique ID
        self.id = id or str(uuid.uuid4())  # Generate a unique ID if not provided
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def get_players(self):
        # Load player objects for the match using their IDs
        p1 = Player.load_by_id(self.player1_id)
        p2 = Player.load_by_id(self.player2_id) if self.player2_id else None
        return p1, p2

    def to_dict(self):
        # Convert the Match object to a dictionary for serialization
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "score1": self.score1,
            "score2": self.score2,
        }

    def save(self):
        # Save the current match to the database (JSON file)
        matches = Match.load_all()  # Load all existing matches
        matches = [m for m in matches if m.id != self.id]  # Remove any existing match with the same ID
        matches.append(self)  # Add the current match
        Match.save_all(matches)  # Save all matches back to the file

    @staticmethod
    def save_all(matches):
        # Save a list of matches to the JSON file
        os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the data directory exists
        with open(MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in matches], f, indent=4)  # Serialize matches to JSON

    @staticmethod
    def load_all():
        # Load all matches from the JSON file
        if not os.path.exists(MATCHES_FILE):
            return []  # Return an empty list if the file doesn't exist
        with open(MATCHES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)  # Load JSON data
            except json.JSONDecodeError:
                return []  # Return an empty list if the file is corrupted
        return [Match(**m) for m in data]  # Deserialize JSON data into Match objects

    @staticmethod
    def load_by_id(match_id):
        # Load a specific match by its ID
        matches = Match.load_all()  # Load all matches
        for m in matches:
            if m.id == match_id:  # Find the match with the given ID
                return m
        return None  # Return None if no match is found

    @staticmethod
    def delete_by_id(match_id):
        # Delete a specific match by its ID
        matches = Match.load_all()  # Load all matches
        matches = [m for m in matches if m.id != match_id]  # Remove the match with the given ID
        Match.save_all(matches)  # Save the updated list of matches
