from datetime import datetime, timedelta
from typing import List

from PyQt5.QtCore import *

from action import Action
import time

# Definition of the Protocol class, which inherits from QRunnable to allow multi-threading
class Protocol(QRunnable):

    def __init__(self):
        super().__init__()
        self.data = []  # List to hold protocol actions (events)
        self.number_repetition = 0  # Number of repetitions for the protocol
        self.time = 0  # Time delay between protocol repetitions
        self.timer = False  # Flag to check if the timer is running
        self.ok = False  # Flag to indicate if the process is running correctly
        self.stop = False  # Flag to stop the protocol

    # Setter for the number of repetitions
    def set_number_repetition(self, number_repetition):
        self.number_repetition = number_repetition

    # Getter for the number of repetitions
    def get_number_repetition(self):
        return self.number_repetition

    # Setter for the time delay between repetitions
    def set_time(self, time):
        self.time = time

    # Getter for the time delay
    def get_time(self):
        return self.time

    # Setter for the event data
    def set_data(self, data):
        self.data = data

    # Getter for the event data
    def get_data(self):
        return self.data

    # Adds a new action/event to the protocol
    def add_data(self, new_element: Action):
        self.data.append(new_element)

    # Setter to control whether the protocol is paused/stopped
    def set_pause(self, stop):
        self.stop = stop

    # Method to execute the protocol actions in order
    def event_go(self):
        self.stop = False  # Resets the stop flag
        self.ok = False  # Resets the "ok" flag

        while not self.stop:  # Loop until the protocol is stopped
            for event in self.data:  # Loop through each event in the protocol
                self.ok = event.toDo()  # Executes the action and stores the result

                if self.stop:  # Break the loop if the stop flag is set
                    print("Stop !")
                    break

                if not self.ok:  # If an event fails, log an error and break
                    print("WARNING : ERROR !")
                    break

                event.info(self.ok)  # Log event info

            self.stop = True  # Once the events are completed, stop the protocol

        return self.ok  # Return whether the execution was successful

    # Slot method to run the protocol in a separate thread
    @pyqtSlot()
    def run(self):
        self.timer = False # Resets the timer flag
        counter = 0  # Initialize the counter for repetitions

        while not self.timer:  # Loop until the timer flag is set
            time0 = datetime.now()  # Record the start time of the protocol

            self.event_go()  # Run the protocol actions

            time1 = datetime.now()  # Record the end time of the protocol
            duration = time1 - time0  # Calculate the duration of the protocol execution
            duration_sec = duration.total_seconds()  # Convert duration to seconds
            delay = (self.time - duration_sec)  # Calculate the remaining time for delay

            # If the counter is less than the number of repetitions, wait for the next iteration
            if counter < self.number_repetition - 1:
                try:
                    time.sleep(delay)  # Wait for the delay time before repeating
                except KeyboardInterrupt:
                    pass

            counter += 1  # Increment the repetition counter

            # If the number of repetitions is reached, stop the timer
            if counter == self.number_repetition:
                self.timer = True
                print("End !!")  # Protocol execution is complete

    # Method to stop the protocol execution
    def stop(self):
        self.ok = False  # Set the "ok" flag to False
        self.timer = True  # Stop the timer
        self.stop = True  # Set the stop flag to True
        print("Interrupt")  # Log that the protocol was interrupted
