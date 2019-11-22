from classes.door import Door
from classes.timecontrol import TimeControl

class ChickenCoop:
    """ChickenCoop object"""

    def __init__(self, timeControl, doors):
        self.doors = doors
        self.timeControl = timeControl