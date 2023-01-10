from enum import Enum
from dataclasses import dataclass
import json

@dataclass
class Spaceship():
    class Alignment(Enum):
        Neutral = 0
        Ally = 1
        Enemy = 2

    class Vessel_class(Enum):
        Corvette = 0
        Frigate = 1
        Cruiser = 2
        Destroyer = 3
        Carrier = 4
        Dreadnought = 5
        Unknown = 6

    alignment: Alignment
    name: str
    vessel_class: Vessel_class
    length: float
    size: int
    armed: bool
    officers: list[dict[str, str]]

    def __init__(self, alignment, name, vessel_class, length, size, armed=False, officers=None):
        if officers is None:
            officers = []
        self.alignment = alignment
        self.name = name
        self.vessel_class = vessel_class
        self.length = length
        self.size = size
        self.armed = armed
        self.officers = officers

    def __dict__(self):
        return {'alignment': self.alignment, 'name': self.name, 'length': self.length, 'vessel_class': self.vessel_class,
                'size': self.size, 'armed': self.armed, 'officers': self.officers}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
