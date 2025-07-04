class Player:
    def __init__(self, chess_id, last_name, first_name, birthdate):
        self.chess_id = chess_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Player(**data)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.chess_id})"
