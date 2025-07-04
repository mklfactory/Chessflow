

class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_time = None
        self.end_time = None

    def add_match(self, match):
        self.matches.append(match)

    def to_dict(self):
        r = {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
        return r

    @staticmethod
    def from_dict(data):
        from models.match import Match
        round_obj = Round(data["name"])
        round_obj.matches = [Match.from_dict(m) for m in data.get("matches", [])]
        round_obj.start_time = data.get("start_time")
        round_obj.end_time = data.get("end_time")
        return round_obj
