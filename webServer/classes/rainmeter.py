import RPi.GPIO as GPIO
import schedule
import time
import threading
import logging
from threading import Thread, RLock

# locker = RLock()

class Rainmeter(Thread):
    """Rainmeter object"""

    tick: int
    gpio: int
    

    def __init__(self, gpio):
        Thread.__init__(self)

        self.tick = 0
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gpio, GPIO.FALLING)

        self.logger = logging.getLogger('chickencoop')
        schedule.clear('rainmeter')
        schedule.every().day.at("22:50").do(self.run_action, 'init').tag('init')
        # schedule.every().day.at("00:00").do(self.run_action, 'init').tag('init')
        self.logger.info('Rainmeter initialized')

    def run_action(self, action):

        if action == 'init':
            # with locker:
            self.tick = 0
            self.logger.info('Rainmeter reinitialized')

    def run(self):
        while True:
            if GPIO.event_detected(self.gpio):
                # with locker:
                self.tick += 1
                self.logger.info('Rainmeter tick detected: ' + str(self.tick))
            schedule.run_pending()
            time.sleep(1)
            

