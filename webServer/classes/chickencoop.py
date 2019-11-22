from classes.door import Door
from classes.timecontrol import TimeControl
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ChickenCoop:
    """ChickenCoop object"""

    doors:Door
    timeControl:TimeControl

    def __init__(self, timeControl, doors):
        self.doors = doors
        self.timeControl = timeControl
