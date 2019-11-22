import RPi.GPIO as GPIO
import time
import logging
from datetime import datetime

# init logger
logFormat='[%(levelname)s] %(asctime)s: %(message)s'
logDateFormat='%d/%m/%Y %H:%M:%S'
logger = logging.getLogger('simple_example')
logging.basicConfig(format=logFormat, datefmt=logDateFormat, filename='./logs/'+datetime.now().strftime("%d_%m_%Y - %H:%M:%S")+'.log',level=logging.DEBUG)

# init console logger
consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(logging.DEBUG)
formatter = logging.Formatter(logFormat, datefmt=logDateFormat)
consoleLogger.setFormatter(formatter)
logger.addHandler(consoleLogger)

# init const
DOOR_TIMEOUT_SEC = 10
PAUSE_MS = 0.1
GPIO_CLOSE_DOOR = 4
GPIO_DOOR_WAY = 17
GPIO_END_CYCLE = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger.info('Start open door script')

# reinit timeout & fin de course
isEndOfCycle = False
startDateTime = datetime.now()
isTimeout = False

# init GPIOs
GPIO.setup(GPIO_CLOSE_DOOR, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(GPIO_DOOR_WAY, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(GPIO_END_CYCLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# basculer moteur
GPIO.output(GPIO_DOOR_WAY, GPIO.HIGH)

# lancer fermeture
GPIO.output(GPIO_CLOSE_DOOR , GPIO.HIGH)

# wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
channel = GPIO.wait_for_edge(GPIO_END_CYCLE, GPIO.RISING, timeout = DOOR_TIMEOUT_SEC * 1000)

# stopper fermeture 
GPIO.output(GPIO_CLOSE_DOOR, GPIO.LOW)

if channel is None:
    logger.error('Closing door timed out!')
else:
    logger.info('Door closed')

## tant que pas timeout & pas fin de course
#while(not isEndOfCycle and not isTimeout):
#    # verifier timeout
#    now = datetime.now()
#    delay =(now - startDateTime).total_seconds()
#    isTimeout = delay > DOOR_TIMEOUT_SEC
#    
#    # verifier fin de course
#    isEndOfCycle = GPIO.input(GPIO_END_CYCLE) == GPIO.HIGH
#    
#    # pause
#    time.sleep(PAUSE_MS)
#
## stopper fermeture 
#GPIO.output(GPIO_CLOSE_DOOR , GPIO.LOW)
#
## si fin de course, remonter ok
#if(isEndOfCycle):
#    logging.info(datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+': Door closed')
#else: # sinon, si timeout, remonter erreur
#    logging.error(datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+': Closing door timed out!')

GPIO.cleanup()
