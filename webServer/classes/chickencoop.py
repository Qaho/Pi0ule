import schedule
import time
import threading
import logging
from threading import Thread

from classes.door import Door
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ChickenCoop(Thread):
    """ChickenCoop object"""

    doors:Door

    openingTime: str
    closingTime: str

    def __init__(self, doors):
        Thread.__init__(self)

        self.doors = doors
        self.openingTime = "06:00"
        self.closingTime = "19:00"

        self.logger = logging.getLogger('chickencoop')


    def __eq__(self, other): return self is other
    def __hash__(self): return hash(id(self))


    def setupOpeningTime(self):
        schedule.clear('opening')
        schedule.every().day.at(self.openingTime).do(self.run_threaded, self.job).tag('opening')


    def setupClosingTime(self):
        schedule.clear('closing')
        schedule.every().day.at(self.closingTime).do(self.run_threaded, self.job).tag('closing')
    

    def run_threaded(self, job_func):

        for d in self.doors:
            job_thread = threading.Thread(target=d.open())
            job_thread.start()


    def job(self):
        self.logger.info("I'm working...")
        return


    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

