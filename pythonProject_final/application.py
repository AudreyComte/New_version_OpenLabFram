# Importing the QtWidgets module from the PyQt5 library
from PyQt5 import QtWidgets

# Importing the Event2 class from the event module
from event import Event2

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Create an instance of the Qt application (required for any PyQt application)
    app = QtWidgets.QApplication([])

    # Create a main window
    fenetre = QtWidgets.QMainWindow()

    # Initialize the user interface with the Event2 class,
    # passing the main window as a parameter
    ui = Event2(fenetre)

    # Display the main window
    fenetre.show()

    # Start the main application loop (to listen for user events)
    app.exec_()
