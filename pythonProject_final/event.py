import sys
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from picamera import PiCamera
from time import sleep
import multiprocessing
import threading
from PyQt5.QtGui import QColor
import arduino
from arduino import Arduino
import mainwindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import re
from QPlainTextEditLogger import QPlainTextEditLogger
from mouvement import Mouvement
# from picture import Picture
from plate import Plate
from protocol import Protocol

# Declaration of the Event2 class, inheriting from the interface defined in mainwindow.Ui_OpenLabFrame
class Event2(mainwindow.Ui_OpenLabFrame):
    someEventOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        # Initialization of protocol and threadpool objects
        self.protocol = Protocol()
        self.threadpool = QThreadPool()
        self.setupUi(parent)

        # Redirecting standard output and errors to a console widget in the interface
        sys.stdout = QPlainTextEditLogger(self.textEdit_console)
        sys.stderr = QPlainTextEditLogger(self.textEdit_console)

        # Initializing and opening the Arduino connection
        self.arduino = Arduino("/dev/ttyACM0")
        self.arduino.open_port()

        # Initializing variables used for plate management and coordinates
        self.plate_6_well = None
        self.table_A1 = [0] * 4

        #self.threadpool = QThreadPool()

        #self.threadpool.start(self.protocol)

        #self.thread = QThread()

        #self.protocol.moveToThread(self.thread)

        # Connecting buttons and sliders to their corresponding methods

        # Button to start and stop the camera
        self.pushButton_start_preview.clicked.connect(self.start_camera)
        self.pushButton_stop_preview.clicked.connect(self.stop_camera)

        # Configuring the limits for the step slider
        self.horizontalSlider_step.setMinimum(0)
        self.horizontalSlider_step.setMaximum(50)
        self.horizontalSlider_step.setSingleStep(1)
        self.horizontalSlider_step.valueChanged.connect(self.update_label)

        # Entering X, Y, X coordinates
        self.lineEdit_x.returnPressed.connect(self.handle_enter_pressed_x)
        self.lineEdit_y.returnPressed.connect(self.handle_enter_pressed_y)
        self.lineEdit_z.returnPressed.connect(self.handle_enter_pressed_z)

        # Decreasing X button
        self.pushButton_moins_x.clicked.connect(self.moinsnumberX)
        self.pushButton_moins_x.setEnabled(False)

        # Decreasing Y button
        self.pushButton_moins_y.clicked.connect(self.moinsnumberY)
        self.pushButton_moins_y.setEnabled(False)

        # Decreasing Z button
        self.pushButton_moins_z.clicked.connect(self.moinsnumberZ)
        self.pushButton_moins_z.setEnabled(False)

        # Increasing X button
        self.pushButton_plus_x.clicked.connect(self.plusnumberX)
        self.pushButton_plus_x.setEnabled(False)

        # Increasing Y button
        self.pushButton_plus_y.clicked.connect(self.plusnumberY)
        self.pushButton_plus_y.setEnabled(False)

        # Increasing Z button
        self.pushButton_plus_z.clicked.connect(self.plusnumberZ)
        self.pushButton_plus_z.setEnabled(False)

        # Set Zero button
        self.pushButton_set_zero.setEnabled(False)
        self.pushButton_set_zero.clicked.connect(lambda: self.send_arduino("G10 P0 L20 X0 Y0 Z0"))
        self.pushButton_set_zero.clicked.connect(self.reset_lcd_numbers)

        # Homing button
        self.pushButton_home.clicked.connect(lambda: self.send_arduino("$h"))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_moins_x.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_plus_x.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_moins_y.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_plus_y.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_moins_z.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_plus_z.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_set_zero.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_reset.setEnabled(True))
        self.pushButton_home.clicked.connect(lambda: self.pushButton_set_as_a1.setEnabled(True))
        self.pushButton_home.clicked.connect(self.reset_lcd_numbers)
        self.pushButton_home.clicked.connect(self.reset_lineEdit_numbers)

        # Reset button
        self.pushButton_reset.setEnabled(False)
        self.pushButton_reset.clicked.connect(lambda: self.send_arduino("G92x0y0z0"))
        self.pushButton_reset.clicked.connect(self.reset_lcd_numbers)
        self.pushButton_reset.clicked.connect(self.reset_lineEdit_numbers)

        # Set as A1 button
        self.pushButton_set_as_a1.setEnabled(False)
        self.pushButton_set_as_a1.clicked.connect(self.set_as_A1)

        # Connecting sliders for image parameters (contrast, brightness, saturation, delay before picture)
        self.label_step_contrast.setText('0')
        self.label_step_brightness.setText('0')
        self.label_step_saturation.setText('0')
        self.label_step_picture_delay.setText('0')
        self.label_step_picture_width.setText('100')
        self.label_step_picture_heigth.setText('100')
        self.horizontalSlider_camera_contrast.valueChanged.connect(self.update_label_contrast)
        self.horizontalSlider_camera_contrast.setMinimum(-100)
        self.horizontalSlider_camera_contrast.setMaximum(100)
        self.horizontalSlider_camera_contrast.setSingleStep(1)
        self.horizontalSlider_camera_brightness.valueChanged.connect(self.update_label_brightness)
        self.horizontalSlider_camera_brightness.setMinimum(0)
        self.horizontalSlider_camera_brightness.setMaximum(100)
        self.horizontalSlider_camera_brightness.setSingleStep(1)
        self.horizontalSlider_camera_saturartion.valueChanged.connect(self.update_label_saturation)
        self.horizontalSlider_camera_saturartion.setMinimum(0)
        self.horizontalSlider_camera_saturartion.setMaximum(100)
        self.horizontalSlider_camera_saturartion.setSingleStep(1)
        self.horizontalSlider_picture_delay.valueChanged.connect(self.update_label_picture_delay)
        self.horizontalSlider_picture_delay.setMinimum(0)
        self.horizontalSlider_picture_delay.setMaximum(300)
        self.horizontalSlider_picture_delay.setSingleStep(1)
        self.horizontalSlider_picture_width.valueChanged.connect(self.update_label_picture_width)
        self.horizontalSlider_picture_width.setMinimum(0)
        self.horizontalSlider_picture_width.setMaximum(100)
        self.horizontalSlider_picture_width.setSingleStep(1)
        self.horizontalSlider_picture_heigth.valueChanged.connect(self.update_label_picture_heigth)
        self.horizontalSlider_picture_heigth.setMinimum(0)
        self.horizontalSlider_picture_heigth.setMaximum(100)
        self.horizontalSlider_picture_heigth.setSingleStep(1)

        # Button to select the wells of a 6-well plate
        self.pushButton_6_well.clicked.connect(self.well6)
        self.pushButton_A1_6_well_plate_1.clicked.connect(self.A1)
        self.pushButton_A2_6_well_plate_1.clicked.connect(self.A2)
        self.pushButton_A3_6_well_plate_1.clicked.connect(self.A3)
        self.pushButton_B1_6_well_plate_1.clicked.connect(self.B1)
        self.pushButton_B2_6_well_plate_1.clicked.connect(self.B2)
        self.pushButton_B3_6_well_plate_1.clicked.connect(self.B3)
        self.pushButton_select_all_well.clicked.connect(self.all_well_6)

        # Button to import a protocol
        self.pushButton_protocol_import.clicked.connect(self.startThread)
        # self.pushButton_add_picture.clicked.connect(self.add_picture())

    # Method to start the camera using a raspistill command via subprocess
    def start_camera(self):
        global preview_process
        command = f"raspistill -t 0 --preview {573},{137},{220},{280}"
        preview_process = subprocess.Popen(command, shell=True)

    # Method to stop camera by killing raspistill process
    def stop_camera(self):
        global preview_process
        if preview_process is not None:
            subprocess.run(["pkill", "raspistill"])

    # Method for selecting step values
    def update_label(self):
        value = self.horizontalSlider_step.value()
        self.label_step_grad.setText(str(value))

    # Method to change the absolute values of x coordinates
    def handle_enter_pressed_x(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^\d*([.,]?\d*)?$', text):
                if 0 <= float(text) < 130:
                    self.send_arduino("G90G0X" + sender.text())

    # Method to change the absolute values of y coordinates
    def handle_enter_pressed_y(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^\d*([.,]?\d*)?$', text):
                if 0 <= float(text) < 90:
                    self.send_arduino("G90G0Y" + sender.text())

    # Method to change the absolute values of z coordinates
    def handle_enter_pressed_z(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^-?\d*([.,]?\d*)?$', text):
                if 0 >= float(text) > -50:
                    self.send_arduino("G90G0Z" + sender.text())

    # Method to decrement X value
    def moinsnumberX(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_x.text())) - float(self.label_step_grad.text()) >= 0:
                self.lcdNumber_x.display(self.lcdNumber_x.value() - float(self.label_step_grad.text()))
                self.lineEdit_x.setText(str(float(self.lineEdit_x.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0X-" + self.label_step_grad.text())

    # Method to increment X value
    def plusnumberX(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_x.text())) + float(self.label_step_grad.text()) < 130:
                self.lcdNumber_x.display(self.lcdNumber_x.value() + float(self.label_step_grad.text()))
                self.lineEdit_x.setText(str(float(self.lineEdit_x.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0X" + self.label_step_grad.text())

    # Method to decrement Y value
    def moinsnumberY(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_y.text())) - float(self.label_step_grad.text()) >= 0:
                self.lcdNumber_y.display(self.lcdNumber_y.value() - float(self.label_step_grad.text()))
                self.lineEdit_y.setText(str(float(self.lineEdit_y.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0Y-" + self.label_step_grad.text())

    # Method to increment Y value
    def plusnumberY(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_y.text())) + float(self.label_step_grad.text()) < 90:
                self.lcdNumber_y.display(self.lcdNumber_y.value() + float(self.label_step_grad.text()))
                self.lineEdit_y.setText(str(float(self.lineEdit_y.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0Y" + self.label_step_grad.text())

    # Method to decrement Z value
    def moinsnumberZ(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_z.text())) - float(self.label_step_grad.text()) > -50:
                self.lcdNumber_z.display(self.lcdNumber_z.value() - float(self.label_step_grad.text()))
                self.lineEdit_z.setText(str(float(self.lineEdit_z.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0Z-" + self.label_step_grad.text())

    # Method to increment Z value
    def plusnumberZ(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_z.text())) + float(self.label_step_grad.text()) <= 0:
                self.lcdNumber_z.display(self.lcdNumber_z.value() + float(self.label_step_grad.text()))
                self.lineEdit_z.setText(str(float(self.lineEdit_z.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0Z" + self.label_step_grad.text())

    # Method to reset the values displayed on the LCDs (relative coordinates)
    def reset_lcd_numbers(self):
        self.lcdNumber_x.display(0)
        self.lcdNumber_y.display(0)
        self.lcdNumber_z.display(0)

    # Method to reset the values in the text fields for coordinates (absolute coordinates)
    def reset_lineEdit_numbers(self):
        self.lineEdit_x.setText(str(0))
        self.lineEdit_y.setText(str(0))
        self.lineEdit_z.setText(str(0))

    # Method to set current X, Y, Z coordinates as position A1 in table table_A1
    def set_as_A1(self):
        self.table_A1[0] = 1
        self.table_A1[1] = self.lcdNumber_x.value()
        self.table_A1[2] = self.lcdNumber_y.value()
        self.table_A1[3] = self.lcdNumber_z.value()

    # Method to send commands to the Arduino via serial port
    def send_arduino(self, gcode):
        self.arduino.write_read(gcode)
        print(gcode + " ok!")

    # Method to update the contrast label with the current value of the contrast slider
    def update_label_contrast(self):
        value = self.horizontalSlider_camera_contrast.value()
        text = str(value)
        self.label_step_contrast.setText(text)

    # Method to update the brightness label with the current value of the brightness slider
    def update_label_brightness(self):
        value = self.horizontalSlider_camera_brightness.value()
        text = str(value)
        self.label_step_brightness.setText(text)

    # Method to update the saturation label with the current value of the saturation slider
    def update_label_saturation(self):
        value = self.horizontalSlider_camera_saturartion.value()
        text = str(value)
        self.label_step_saturation.setText(text)

    # Method to update the delay label with the current value of the delay slider
    def update_label_picture_delay(self):
        value = self.horizontalSlider_picture_delay.value()
        text = str(value)
        self.label_step_picture_delay.setText(text)

    # Method to update the width label with the current value of the width slider
    def update_label_picture_width(self):
        value = self.horizontalSlider_picture_width.value()
        text = str(value)
        self.label_step_picture_width.setText(text)

    # Method to update the heigth label with the current value of the heigth slider
    def update_label_picture_heigth(self):
        value = self.horizontalSlider_picture_heigth.value()
        text = str(value)
        self.label_step_picture_heigth.setText(text)

    # Method to change the color of selected 6-well plate
    # and to configure wells coordinates, including A1 if defined
    def well6(self):
        # Create a QColor object with RGB values for light gray
        color = QColor(192, 192, 192)

        # Check if the current button color is not equal to the defined gray color
        if not self.pushButton_6_well.palette().button().color() == color:
            # If the button is not gray, set its background color to gray using a style sheet
            self.pushButton_6_well.setStyleSheet("background-color: {}".format(color.name()))
            # Create an instance of a 6-well plate
            self.plate_6_well = Plate(6)
            # Initialize the 6-well plate
            self.plate_6_well.well_6()
            # If the A1 position is set (table_A1[0] == 1), assign the saved X, Y, Z coordinates to the plate
            if self.table_A1[0] == 1:
                self.plate_6_well.A1_x = self.table_A1[1]
                self.plate_6_well.A1_y = self.table_A1[2]
                self.plate_6_well.A1_z = self.table_A1[3]
            # Calculate and apply the coordinates for the wells
            self.plate_6_well.coordinate_well()
        else:
            # If the button is already gray, reset its style sheet (removing the gray background)
            self.pushButton_6_well.setStyleSheet("")

    # Method to manage the color change for the A1 button when selected
    # and to add the movement data for the A1 well to the protocol
    def A1(self):
        # Create a QColor object with RGB values for light gray
        color = QColor(192, 192, 192)
        # Check if the current button color is not equal to the defined gray color
        if not self.pushButton_A1_6_well_plate_1.palette().button().color() == color:
            # If the button is not gray, set its background color to gray using a style sheet
            self.pushButton_A1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            # Check if the 6-well plate object exists
            if self.plate_6_well is not None:
                # Create a movement object with the X, Y, Z coordinates of well A1 from the plate
                mouvement = Mouvement(self.plate_6_well.tx[1], self.plate_6_well.ty[1], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                # Add the movement data to the protocol
                self.protocol.add_data(mouvement)

        else:
            # If the button is already gray, reset its style sheet (removing the gray background)
            self.pushButton_A1_6_well_plate_1.setStyleSheet("")

    # Method to manage the color change for the A2 button when selected
    # and to add the movement data for the A2 well to the protocol
    def A2(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_A2_6_well_plate_1.palette().button().color() == color:
            self.pushButton_A2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[2], self.plate_6_well.ty[1], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)
        else:
            self.pushButton_A2_6_well_plate_1.setStyleSheet("")

    # Method to manage the color change for the A3 button when selected
    # and to add the movement data for the A3 well to the protocol
    def A3(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_A3_6_well_plate_1.palette().button().color() == color:
            self.pushButton_A3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[3], self.plate_6_well.ty[1], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)
        else:
            self.pushButton_A3_6_well_plate_1.setStyleSheet("")

    # Method to manage the color change for the B1 button when selected
    # and to add the movement data for the B1 well to the protocol
    def B1(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_B1_6_well_plate_1.palette().button().color() == color:
            self.pushButton_B1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[1], self.plate_6_well.ty[2], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)
        else:
            self.pushButton_B1_6_well_plate_1.setStyleSheet("")

    # Method to manage the color change for the B2 button when selected
    # and to add the movement data for the B2 well to the protocol
    def B2(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_B2_6_well_plate_1.palette().button().color() == color:
            self.pushButton_B2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[2], self.plate_6_well.ty[2], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)
        else:
            self.pushButton_B2_6_well_plate_1.setStyleSheet("")

    # Method to manage the color change for the B3 button when selected
    # and to add the movement data for the B3 well to the protocol
    def B3(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_B3_6_well_plate_1.palette().button().color() == color:
            self.pushButton_B3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[3], self.plate_6_well.ty[2], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)
        else:
            self.pushButton_B3_6_well_plate_1.setStyleSheet("")

    # Method to select all wells, change their color
    # and add the movement data for each well to the protocol
    def all_well_6(self):
        # Create a QColor object with RGB values for light gray
        color = QColor(192, 192, 192)
        # Check if the current button color is not equal to the defined gray color
        if not self.pushButton_select_all_well.palette().button().color() == color:
            # If the button is not gray, set its background color to gray using a style sheet
            self.pushButton_select_all_well.setStyleSheet("background-color: {}".format(color.name()))
            # Set the background color of all well buttons (A1, A2, A3, B1, B2, B3) to gray
            self.pushButton_A1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_A2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_A3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            # If the 6-well plate object exists
            if self.plate_6_well is not None:
                # Loop through each row (r) and column (c) of the wells in the 6-well plate
                for r in range(1, len(self.plate_6_well.ty)):
                    for c in range(1, len(self.plate_6_well.tx)):
                        # Create a movement object with the X, Y, Z coordinates of the current well
                        mouvement = Mouvement(self.plate_6_well.tx[c], self.plate_6_well.ty[r], self.plate_6_well.A1_z,
                                              self.arduino)
                        # mouvement.toDo()
                        # Add the movement to the protocol
                        self.protocol.add_data(mouvement)
        else:
            # If the button is already gray, reset the style sheet of the "select all" button and all well buttons
            self.pushButton_select_all_well.setStyleSheet("")
            self.pushButton_select_all_well.setStyleSheet("")
            self.pushButton_A1_6_well_plate_1.setStyleSheet("")
            self.pushButton_A2_6_well_plate_1.setStyleSheet("")
            self.pushButton_A3_6_well_plate_1.setStyleSheet("")
            self.pushButton_B1_6_well_plate_1.setStyleSheet("")
            self.pushButton_B2_6_well_plate_1.setStyleSheet("")
            self.pushButton_B3_6_well_plate_1.setStyleSheet("")

    # def add_picture(self):
    #     picture = Picture(int(self.label_step_contrast.text()), int(self.label_step_brightness.text()),
    #                       int(self.label_step_saturation.text()), int(self.label_step_picture_delay.text()),
    #                       int(self.label_step_picture_width.text()), int(self.label_step_picture_heigth.text()))
    #     picture.toDo()

    # def start_protocol(self):
    #     for element in self.protocol.data:
    #         print(element)
    #     self.protocol.event_go()

    # Method to initialize the number of repetitions and the time interval
    # and start the protocol in a separate thread.
    def startThread(self):
        # Check if the "number of repetitions" field is empty
        if self.lineEdit_number_repetition.text() == "":
            # If empty, set it to "1" as a default value
            self.lineEdit_number_repetition.setText("1")

            # Check if the "protocol times repetitions" field is empty
            if self.lineEdit_protocol_times_repetitions.text() == "":
                # If empty, set it to "0" as a default value
                self.lineEdit_protocol_times_repetitions.setText("0")

            # Set the number of repetitions in the protocol based on the input field
            self.protocol.set_number_repetition(int(self.lineEdit_number_repetition.text()))
            # Set the time between protocol repetitions based on the input field
            self.protocol.set_time(int(self.lineEdit_protocol_times_repetitions.text()))

        # Start the protocol in a separate thread using the thread pool
        self.threadpool.start(self.protocol)


    # def start_timer2(self):
    #     self.threadpool.start(self.start_timer)
    #
    # def start_timer(self):
    #     if self.lineEdit_number_repetition.text() == "":
    #         self.lineEdit_number_repetition.setText("1")
    #
    #     if self.lineEdit_protocol_times_repetitions.text() == "":
    #         self.lineEdit_protocol_times_repetitions.setText("0")
    #
    #     self.protocol.set_number_repetition(int(self.lineEdit_number_repetition.text()))
    #     self.protocol.set_time(int(self.lineEdit_protocol_times_repetitions.text()))
    #
    #     self.protocol.run()

        #t1 = multiprocessing.Process(target=self.protocol.run())
        #
        # # t1 = threading.Thread(target=self.protocol.run())
        # t1.start()
        # t1.join()

    # def start_timer(self):
    #
    #     if self.lineEdit_number_repetition.text() == "":
    #         (self.lineEdit_number_repetition.setText("1"))
    #
    #     if self.lineEdit_protocol_times_repetitions.text() == "":
    #         (self.lineEdit_protocol_times_repetitions.setText("0"))
    #
    #     t1 = threading.Thread(target=self.protocol.run())
    #
    #     self.protocol.set_number_repetition(int(self.lineEdit_number_repetition.text()))
    #     self.protocol.set_time(int(self.lineEdit_protocol_times_repetitions.text()))
    #
    #     self.protocol.run()
    #
    #     t1.start()
