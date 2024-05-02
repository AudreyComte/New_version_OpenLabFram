from datetime import datetime, timedelta
from typing import List

from PyQt5.QtCore import *

from action import Action
import time


class Protocol(QRunnable):

    def __init__(self):
        super().__init__()
        self.data = []
        self.number_repetition = 0
        self.time = 0
        self.timer = False
        self.ok = False
        self.stop = False

    def set_number_repetition(self, number_repetition):
        self.number_repetition = number_repetition

    def get_number_repetition(self):
        return self.number_repetition

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def add_data(self, new_element: Action):
        self.data.append(new_element)

    def set_pause(self, stop):
        self.stop = stop

    def event_go(self):
        self.stop = False
        self.ok = False

        while not self.stop:
            for event in self.data:
                self.ok = event.toDo()

                if self.stop:
                    print("Stop !")
                    break

                if not self.ok:
                    print("WARNING : ERROR !")
                    break

                event.info(self.ok)

            self.stop = True

        return self.ok

    @pyqtSlot()
    def run(self):
        self.timer = False
        counter = 0

        while not self.timer:
            time0 = datetime.now()

            self.event_go()

            time1 = datetime.now()
            duration = time1 - time0
            duration_sec = duration.total_seconds()
            delay = (self.time - duration_sec)

            if counter < self.number_repetition - 1:
                try:
                    time.sleep(delay)
                except KeyboardInterrupt:
                    pass

            counter += 1

            if counter == self.number_repetition:
                self.timer = True
                print("End !!")

    def stop(self):
        self.ok = False
        self.timer = True
        self.stop = True
        print("Interrupt")
