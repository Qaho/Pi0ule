import RPi.GPIO as GPIO
import logging
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_LEVEL_CLOSE = GPIO.HIGH
GPIO_LEVEL_OPEN = GPIO.LOW

class Status(Enum):
        OPENED = "OPENED"
        OPENING = "OPENING"
        OPENING_ERROR = "OPENING_ERROR"
        CLOSED = "CLOSED"
        CLOSING = "CLOSING"
        CLOSING_ERROR = "CLOSING_ERROR"
        UNKNOWN = "UNKNOWN"

@dataclass_json
@dataclass
class Door:

    name: str

    isOpened: bool
    isClosed: bool

    gpioIsOpened: int
    gpioIsClosed: int
    gpioOpenCloseWay:int
    gpioRun:int

    timeoutOpening: int
    timeoutClosing: int

    status: Status

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
        
        self.gpioIsOpened = gpioIsOpened
        self.gpioIsClosed = gpioIsClosed
        self.gpioOpenCloseWay = gpioOpenCloseWay
        self.gpioRun = gpioRun

        self.timeoutOpening = 10
        self.timeoutClosing = 10

        self.status = Status.UNKNOWN

        if(self.isOpened):
            self.status = Status.OPENED
        elif (self.isClosed):
            self.status = Status.CLOSED

        self.logger = logging.getLogger('chickencoop')

    def open(self):

        if(self.status == Status.OPENED):
            self.logger.info('Door already opened')
        elif(self.status == Status.OPENING):
            self.logger.info('Door already opening')
        else:
            self.logger.info('Opening door "' + self.name + '"...')

            self.status = Status.OPENING

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
                self.status = Status.OPENING_ERROR
            else:
                self.logger.info('Door opened')
                self.status = Status.OPENED

    def close(self):

        if(self.status == Status.CLOSED):
            self.logger.info('Door already closed')
        elif(self.status == Status.CLOSING):
            self.logger.info('Door already closing')
        else:
            self.logger.info('Closing door "' + self.name + '"...')
            self.status = Status.CLOSING

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
                self.status = Status.CLOSING_ERROR
            else:
                self.logger.info('Door closed')
                self.status = Status.CLOSED

    


        