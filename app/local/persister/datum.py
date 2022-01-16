import uuid
from json import JSONEncoder


class Datum:
    def __init__(self, outcome, features):
        self.outcome = outcome
        self.features = features


class DatumEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
