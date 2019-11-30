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

    def __setattr__(self, id, val):
        object.__setattr__(self, id, val)

        if id == "openingTime":
            schedule.clear('opening')
            schedule.every().day.at(self.openingTime).do(self.run_threaded, 'open').tag('opening')
        elif id == "closingTime":
            schedule.clear('closing')
            schedule.every().day.at(self.closingTime).do(self.run_threaded, 'close').tag('closing')

    def run_threaded(self, action, doorid=None):

        for d in self.doors:

            if doorid == None or doorid == d.id:
                if action == 'open':
                    job_thread = threading.Thread(target=d.open())
                    job_thread.start()
                elif action == 'close':
                    job_thread = threading.Thread(target=d.close())
                    job_thread.start()
                elif action == 'stop':
                    job_thread = threading.Thread(target=d.stop())
                    job_thread.start()

    def handleDoorAction(self, doorid, action):
    	
        #get device
        deviceFound = None
        for d in self.doors:
            if d.id == doorid:
                deviceFound = d
                break   

        #handle action on door
        if deviceFound != None:
            if action == "open":
                self.run_threaded('open', deviceFound.id)
            if action == "close":
                self.run_threaded('close', deviceFound.id)
            if action == "stop":
                self.run_threaded('stop', deviceFound.id)

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

