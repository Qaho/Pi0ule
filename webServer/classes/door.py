import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Door:
    """Door object"""

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

        