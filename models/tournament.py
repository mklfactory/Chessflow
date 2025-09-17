import json
import os
import uuid
from datetime import datetime
from models.match import Match

# File path for storing round data
ROUNDS_FILE = "data/rounds.json"


class Round:
    def __init__(self, name, round_id=None, match_ids=None, start_time=None, end_time=None):
        # Initialize a Round object with a name, unique ID, match IDs, start time, and end time
        self.id = round_id or str(uuid.uuid4())  # Generate a unique ID if not provided
        self.name = name  # Name of the round
        self.match_ids = match_ids or []  # List of match IDs associated with the round
        self.start_time = start_time  # Start time of the round
        self.end_time = end_time  # End time of the round

    @property
    def matches(self):
        # Retrieve all matches associated with this round
        all_matches = Match.load_all()  # Load all matches from storage
        return [m for m in all_matches if m.id in self.match_ids]  # Filter matches by match IDs

    def add_match(self, match):
        # Add a match to the round
        if match.id not in self.match_ids:  # Check if the match is not already added
            self.match_ids.append(match.id)  # Add the match ID to the list
            match.save()  # Save the match to storage
            self.save()  # Save the updated round to storage

    def to_dict(self):
        # Convert the Round object to a dictionary for serialization
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data):
        # Create a Round object from a dictionary
        return cls(
            name=data.get("name", ""),  # Get the name of the round
            round_id=data.get("id"),  # Get the round ID
            match_ids=data.get("match_ids", []),  # Get the list of match IDs
            start_time=data.get("start_time"),  # Get the start time
            end_time=data.get("end_time")  # Get the end time
        )

    def save(self):
        # Save the current round to the database (JSON file)
        rounds = Round.load_all()  # Load all existing rounds
        rounds = [r for r in rounds if r.id != self.id]  # Remove any existing round with the same ID
        rounds.append(self)  # Add the current round
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            # Serialize all rounds to JSON and save to the file
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        # Load all rounds from the JSON file
        if not os.path.exists(ROUNDS_FILE):  # Check if the file exists
            return []  # Return an empty list if the file doesn't exist
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)  # Load JSON data
                return [Round.from_dict(d) for d in data]  # Deserialize JSON data into Round objects
            except json.JSONDecodeError:
                return []  # Return an empty list if the file is corrupted

    @staticmethod
    def load_by_id(round_id):
        # Load a specific round by its ID
        for r in Round.load_all():  # Iterate through all rounds
            if r.id == round_id:  # Find the round with the given ID
                return r  # Return the round if found
        return None  # Return None if no round is found

    def start_round(self):
        # Set the start time of the round to the current time
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()  # Save the updated round to storage

    def end_round(self):
        # Set the end time of the round to the current time
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()  # Save the updated round
