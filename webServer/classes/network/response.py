from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

class Status(Enum):
    OK = "OK"
    ERROR = "ERROR"

@dataclass_json
@dataclass
class Response():
    status:Status
    data:object

    def __init__(self, status, data):
        self.status = status
        self.data = data



