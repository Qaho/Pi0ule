import RPi.GPIO as GPIO
import logging
from dataclasses import dataclass
from dataclasses_json import dataclass_json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_LEVEL_CLOSE = GPIO.HIGH
GPIO_LEVEL_OPEN = GPIO.LOW

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

    timeoutOpening: int
    timeoutClosing: int

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

        self.timeoutOpening = 10
        self.timeoutClosing = 10

        self.logger = logging.getLogger('chickencoop')

    def open(self):
        self.logger.info('Opening door "' + self.name + '"...')

        # basculer moteur
        GPIO.output(self.gpioOpenCloseWay, GPIO_LEVEL_OPEN)

        # lancer ouverture
        GPIO.output(self.gpioRun , GPIO.HIGH)

        # attendre timeout
        channel = GPIO.wait_for_edge(self.gpioIsOpened, GPIO.RISING, timeout = self.timeoutOpening * 1000)

        # stopper ouverture 
        GPIO.output(self.gpioRun, GPIO.LOW)

        if channel is None:
            self.logger.error('Opening door timed out!')
        else:
            self.logger.info('Door opened')

    def close(self):
        self.logger.info('Closing door "' + self.name + '"...')

        # basculer moteur
        GPIO.output(self.gpioOpenCloseWay, GPIO_LEVEL_CLOSE)

        # lancer fermeture
        GPIO.output(self.gpioRun , GPIO.HIGH)

        # attendre timeout
        channel = GPIO.wait_for_edge(self.gpioIsClosed, GPIO.RISING, timeout = self.timeoutClosing * 1000)

        # stopper fermeture 
        GPIO.output(self.gpioRun, GPIO.LOW)

        if channel is None:
            self.logger.error('Closing door timed out!')
        else:
            self.logger.info('Door closed')


        