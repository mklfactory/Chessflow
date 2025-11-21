import json
import uuid
import re

DATA_FILE = "data/players.json"
ID_PATTERN = re.compile(r"^[A-Za-z]{2}\d{5}$")

class Player:
    """
    Represents a player with personal information and provides management operations on player data stored in a JSON file.
    """

    def __init__(self, id=None, first_name="", last_name="", birth_date="", gender="", national_id=""):
        """
        Initialize a new Player instance.

        Args:
            id (str): Unique ID of the player. Generated if not provided.
            first_name (str): Player's first name.
            last_name (str): Player's last name.
            birth_date (str): Player's birth date.
            gender (str): Player's gender.
            national_id (str): Player's national identifier.
        """
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.national_id = national_id

    def to_dict(self):
        """
        Convert the Player object into a dictionary representation.

        Returns:
            dict: Dictionary of player attributes.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "national_id": self.national_id,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Player instance from a dictionary.

        Args:
            data (dict): Dictionary of player properties.

        Returns:
            Player: Instance of Player class.
        """
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            birth_date=data.get("birth_date", ""),
            gender=data.get("gender", ""),
            national_id=data.get("national_id", "")
        )

    def save(self):
        """
        Save or update the player in the JSON file.
        """
        players = self.__class__.load_all()
        players = [p for p in players if p.id != self.id]
        players.append(self)
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    @classmethod
    def load_all(cls):
        """
        Load all players from the JSON file.

        Returns:
            list: List of Player instances.
        """
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            return [cls.from_dict(p) for p in data]
        except Exception:
            return []

    @classmethod
    def load_by_id(cls, player_id):
        """
        Get a player by their unique ID.

        Args:
            player_id (str): Player's unique ID.

        Returns:
            Player or None: Player instance if found, None otherwise.
        """
        players = cls.load_all()
        for p in players:
            if p.id == player_id:
                return p
        return None

    @classmethod
    def delete(cls, player_id):
        """
        Delete a player from the JSON file using their unique ID.

        Args:
            player_id (str): ID of the player to delete.
        """
        players = cls.load_all()
        players = [p for p in players if p.id != player_id]
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    def full_name(self):
        """
        Return the full name of the player.

        Returns:
            str: Full name of the player.
        """
        return f"{self.last_name} {self.first_name}".strip()

    @classmethod
    def sort_alphabetically(cls, players):
        """
        Sort a list of Player instances alphabetically by last name and first name.

        Args:
            players (list): List of Player instances.

        Returns:
            list: Alphabetically sorted list.
        """
        return sorted(players, key=lambda p: (p.last_name.lower(), p.first_name.lower()))

    @staticmethod
    def is_valid_national_id(value: str) -> bool:
        """
        Check if the national ID is valid according to the required pattern.

        Args:
            value (str): National ID to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return bool(ID_PATTERN.match(value or ""))
