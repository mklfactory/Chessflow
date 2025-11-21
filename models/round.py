import json
import os
import uuid
from datetime import datetime
from models.match import Match

ROUNDS_FILE = "data/rounds.json"

class Round:
    """
    Represents a round in a tournament, containing matches with associated metadata and methods for persistence.
    """

    def __init__(self, name, round_id=None, match_ids=None, start_time=None, end_time=None):
        """
        Initialize a Round instance.

        Args:
            name (str): Name of the round.
            round_id (str, optional): Unique ID of the round. Generated if not provided.
            match_ids (list, optional): List of match IDs for matches in the round.
            start_time (str, optional): Start time of the round.
            end_time (str, optional): End time of the round.
        """
        self.id = round_id or str(uuid.uuid4())
        self.name = name
        self.match_ids = match_ids or []
        self.start_time = start_time
        self.end_time = end_time

    @property
    def matches(self):
        """
        Retrieve all Match instances associated with this round.

        Returns:
            list: List of Match instances.
        """
        all_matches = Match.load_all()
        return [m for m in all_matches if m.id in self.match_ids]

    def add_match(self, match):
        """
        Add a Match to the round and persist the change.

        Args:
            match (Match): Match instance to add.
        """
        if match.id not in self.match_ids:
            self.match_ids.append(match.id)
            match.save()
            self.save()

    def to_dict(self):
        """
        Convert the Round instance to a dictionary for serialization.

        Returns:
            dict: Dictionary representing the round.
        """
        return {
            "id": self.id,
            "name": self.name,
            "match_ids": self.match_ids,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Round instance from a dictionary.

        Args:
            data (dict): Dictionary of round attributes.

        Returns:
            Round: Instance of Round class.
        """
        return cls(
            name=data.get("name", ""),
            round_id=data.get("id"),
            match_ids=data.get("match_ids", []),
            start_time=data.get("start_time"),
            end_time=data.get("end_time")
        )

    def save(self):
        """
        Save or update the round in the JSON file.
        """
        rounds = Round.load_all()
        rounds = [r for r in rounds if r.id != self.id]
        rounds.append(self)
        with open(ROUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rounds], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all():
        """
        Load all rounds from the JSON file.

        Returns:
            list: List of Round instances.
        """
        if not os.path.exists(ROUNDS_FILE):
            return []
        with open(ROUNDS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Round.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    @staticmethod
    def load_by_id(round_id):
        """
        Retrieve a round by its unique ID.

        Args:
            round_id (str): Unique round ID.

        Returns:
            Round or None: Round instance if found, None otherwise.
        """
        for r in Round.load_all():
            if r.id == round_id:
                return r
        return None

    def start_round(self):
        """
        Set the start time of the round to the current time and persist the change.
        """
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def end_round(self):
        """
        Set the end time of the round to the current time and persist the change.
        """
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()
