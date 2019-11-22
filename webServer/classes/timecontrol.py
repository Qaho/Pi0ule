from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TimeControl:
    """TimeControl object"""

    openingTime: str
    closingTime: str

    def __init__(self):
        """Init"""

        self.openingTime = "6:00"
        self.closingTime = "19:00"
