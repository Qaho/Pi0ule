import RPi.GPIO as GPIO
from dataclasses import dataclass
from dataclasses_json import dataclass_json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

@dataclass_json
@dataclass
class Door:
    """Door object"""
    name: str

    isOpened: bool
    isClosed: bool
    isOpening: bool
    isClosing: bool

    gpioIsOpened: int
    gpioIsClosed: int
    gpioOpenCloseWay:int
    gpioRun:int

    def __init__(self, name, gpioRun, gpioOpenCloseWay, gpioIsOpened, gpioIsClosed):
        """Init"""
        # init GPIOs
        GPIO.setup(gpioRun, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(gpioOpenCloseWay, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(gpioIsClosed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(gpioIsOpened, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.name = name

        self.isOpened = GPIO.input(gpioIsOpened)
        self.isClosed = GPIO.input(gpioIsClosed)
        self.isOpening = False
        self.isClosing = False
        
        self.gpioIsOpened = gpioIsOpened
        self.gpioIsClosed = gpioIsClosed
        self.gpioOpenCloseWay = gpioOpenCloseWay
        self.gpioRun = gpioRun

        