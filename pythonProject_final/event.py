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


class Event2(mainwindow.Ui_OpenLabFrame):
    someEventOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.protocol = Protocol()
        self.threadpool = QThreadPool()
        self.setupUi(parent)

        sys.stdout = QPlainTextEditLogger(self.textEdit_console)
        sys.stderr = QPlainTextEditLogger(self.textEdit_console)

        self.arduino = Arduino("/dev/ttyACM0")
        self.arduino.open_port()

        self.plate_6_well = None
        self.table_A1 = [0] * 4

        #self.threadpool = QThreadPool()

        #self.threadpool.start(self.protocol)

        #self.thread = QThread()

        #self.protocol.moveToThread(self.thread)

        self.pushButton_start_preview.clicked.connect(self.start_camera)
        self.pushButton_stop_preview.clicked.connect(self.stop_camera)
        self.horizontalSlider_step.setMinimum(0)
        self.horizontalSlider_step.setMaximum(50)
        self.horizontalSlider_step.setSingleStep(1)
        self.horizontalSlider_step.valueChanged.connect(self.update_label)
        self.lineEdit_x.returnPressed.connect(self.handle_enter_pressed_x)
        self.lineEdit_y.returnPressed.connect(self.handle_enter_pressed_y)
        self.lineEdit_z.returnPressed.connect(self.handle_enter_pressed_z)
        self.pushButton_moins_x.clicked.connect(self.moinsnumberX)
        self.pushButton_moins_x.setEnabled(False)
        self.pushButton_moins_y.clicked.connect(self.moinsnumberY)
        self.pushButton_moins_y.setEnabled(False)
        self.pushButton_moins_z.clicked.connect(self.moinsnumberZ)
        self.pushButton_moins_z.setEnabled(False)
        self.pushButton_plus_x.clicked.connect(self.plusnumberX)
        self.pushButton_plus_x.setEnabled(False)
        self.pushButton_plus_y.clicked.connect(self.plusnumberY)
        self.pushButton_plus_y.setEnabled(False)
        self.pushButton_plus_z.clicked.connect(self.plusnumberZ)
        self.pushButton_plus_z.setEnabled(False)
        self.pushButton_set_zero.setEnabled(False)
        self.pushButton_set_zero.clicked.connect(lambda: self.send_arduino(
            "G10 P0 L20 X0 Y0 Z0"))  # Button set zero connect #############################################################
        self.pushButton_set_zero.clicked.connect(self.reset_lcd_numbers)
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
        self.pushButton_home.clicked.connect(
            self.reset_lineEdit_numbers)  # Button Home connect #######################################################################################
        self.pushButton_reset.setEnabled(False)
        self.pushButton_reset.clicked.connect(lambda: self.send_arduino(
            "G92x0y0z0"))  # Button Reset connect ##############################################################################
        self.pushButton_reset.clicked.connect(self.reset_lcd_numbers)
        self.pushButton_reset.clicked.connect(self.reset_lineEdit_numbers)
        self.pushButton_set_as_a1.setEnabled(False)
        self.pushButton_set_as_a1.clicked.connect(self.set_as_A1)
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
        self.pushButton_6_well.clicked.connect(self.well6)
        self.pushButton_A1_6_well_plate_1.clicked.connect(self.A1)
        self.pushButton_A2_6_well_plate_1.clicked.connect(self.A2)
        self.pushButton_A3_6_well_plate_1.clicked.connect(self.A3)
        self.pushButton_B1_6_well_plate_1.clicked.connect(self.B1)
        self.pushButton_B2_6_well_plate_1.clicked.connect(self.B2)
        self.pushButton_B3_6_well_plate_1.clicked.connect(self.B3)
        self.pushButton_select_all_well.clicked.connect(self.all_well_6)
        self.pushButton_protocol_import.clicked.connect(self.startThread)
        # self.pushButton_add_picture.clicked.connect(self.add_picture())

    def start_camera(self):
        global preview_process
        command = f"raspistill -t 0 --preview {573},{137},{220},{280}"
        preview_process = subprocess.Popen(command, shell=True)

    def stop_camera(self):
        global preview_process
        if preview_process is not None:
            subprocess.run(["pkill", "raspistill"])

    # Valeurs des step

    def update_label(self):
        value = self.horizontalSlider_step.value()
        self.label_step_grad.setText(str(value))

    # Modification des valeurs absolue en x
    def handle_enter_pressed_x(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^\d*([.,]?\d*)?$', text):
                if 0 <= float(text) < 130:
                    self.send_arduino("G90G0X" + sender.text())

    # Modification des valeurs absolue en y
    def handle_enter_pressed_y(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^\d*([.,]?\d*)?$', text):
                if 0 <= float(text) < 90:
                    self.send_arduino("G90G0Y" + sender.text())

    # Modification des valeurs absolue en z
    def handle_enter_pressed_z(self):
        sender = self.tab_preview.focusWidget()
        if isinstance(sender, QtWidgets.QLineEdit):
            text = sender.text()
            if re.match(r'^-?\d*([.,]?\d*)?$', text):
                if 0 >= float(text) > -50:
                    self.send_arduino("G90G0Z" + sender.text())

    def moinsnumberX(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_x.text())) - float(self.label_step_grad.text()) >= 0:
                self.lcdNumber_x.display(self.lcdNumber_x.value() - float(self.label_step_grad.text()))
                self.lineEdit_x.setText(str(float(self.lineEdit_x.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0X-" + self.label_step_grad.text())

    def plusnumberX(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_x.text())) + float(self.label_step_grad.text()) < 130:
                self.lcdNumber_x.display(self.lcdNumber_x.value() + float(self.label_step_grad.text()))
                self.lineEdit_x.setText(str(float(self.lineEdit_x.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0X" + self.label_step_grad.text())

    def moinsnumberY(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_y.text())) - float(self.label_step_grad.text()) >= 0:
                self.lcdNumber_y.display(self.lcdNumber_y.value() - float(self.label_step_grad.text()))
                self.lineEdit_y.setText(str(float(self.lineEdit_y.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0Y-" + self.label_step_grad.text())

    def plusnumberY(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_y.text())) + float(self.label_step_grad.text()) < 90:
                self.lcdNumber_y.display(self.lcdNumber_y.value() + float(self.label_step_grad.text()))
                self.lineEdit_y.setText(str(float(self.lineEdit_y.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0Y" + self.label_step_grad.text())

    def moinsnumberZ(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_z.text())) - float(self.label_step_grad.text()) > -50:
                self.lcdNumber_z.display(self.lcdNumber_z.value() - float(self.label_step_grad.text()))
                self.lineEdit_z.setText(str(float(self.lineEdit_z.text()) - float(self.label_step_grad.text())))
                self.send_arduino("G91G0Z-" + self.label_step_grad.text())

    def plusnumberZ(self):
        if self.label_step_grad.text().strip():
            if (float(self.lineEdit_z.text())) + float(self.label_step_grad.text()) <= 0:
                self.lcdNumber_z.display(self.lcdNumber_z.value() + float(self.label_step_grad.text()))
                self.lineEdit_z.setText(str(float(self.lineEdit_z.text()) + float(self.label_step_grad.text())))
                self.send_arduino("G91G0Z" + self.label_step_grad.text())

    def reset_lcd_numbers(self):
        self.lcdNumber_x.display(0)
        self.lcdNumber_y.display(0)
        self.lcdNumber_z.display(0)

    def reset_lineEdit_numbers(self):
        self.lineEdit_x.setText(str(0))
        self.lineEdit_y.setText(str(0))
        self.lineEdit_z.setText(str(0))

    def set_as_A1(self):
        self.table_A1[0] = 1
        self.table_A1[1] = self.lcdNumber_x.value()
        self.table_A1[2] = self.lcdNumber_y.value()
        self.table_A1[3] = self.lcdNumber_z.value()

    def send_arduino(self, gcode):
        self.arduino.write_read(gcode)
        print(gcode + " ok!")

    # Valeurs des steps contrast
    def update_label_contrast(self):
        value = self.horizontalSlider_camera_contrast.value()
        text = str(value)
        self.label_step_contrast.setText(text)

    # Valeurs des steps brightness
    def update_label_brightness(self):
        value = self.horizontalSlider_camera_brightness.value()
        text = str(value)
        self.label_step_brightness.setText(text)

    # Valeurs des steps saturation
    def update_label_saturation(self):
        value = self.horizontalSlider_camera_saturartion.value()
        text = str(value)
        self.label_step_saturation.setText(text)

    # Valeurs des steps delay
    def update_label_picture_delay(self):
        value = self.horizontalSlider_picture_delay.value()
        text = str(value)
        self.label_step_picture_delay.setText(text)

    # Valeurs des steps width
    def update_label_picture_width(self):
        value = self.horizontalSlider_picture_width.value()
        text = str(value)
        self.label_step_picture_width.setText(text)

    # Valeurs des steps width
    def update_label_picture_heigth(self):
        value = self.horizontalSlider_picture_heigth.value()
        text = str(value)
        self.label_step_picture_heigth.setText(text)

    def well6(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_6_well.palette().button().color() == color:
            self.pushButton_6_well.setStyleSheet("background-color: {}".format(color.name()))
            self.plate_6_well = Plate(6)
            self.plate_6_well.well_6()
            if self.table_A1[0] == 1:
                self.plate_6_well.A1_x = self.table_A1[1]
                self.plate_6_well.A1_y = self.table_A1[2]
                self.plate_6_well.A1_z = self.table_A1[3]
            self.plate_6_well.coordinate_well()
        else:
            self.pushButton_6_well.setStyleSheet("")

    def A1(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_A1_6_well_plate_1.palette().button().color() == color:
            self.pushButton_A1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                mouvement = Mouvement(self.plate_6_well.tx[1], self.plate_6_well.ty[1], self.plate_6_well.A1_z,
                                      self.arduino)
                # mouvement.toDo()
                self.protocol.add_data(mouvement)

        else:
            self.pushButton_A1_6_well_plate_1.setStyleSheet("")

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

    def all_well_6(self):
        color = QColor(192, 192, 192)
        if not self.pushButton_select_all_well.palette().button().color() == color:
            self.pushButton_select_all_well.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_A1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_A2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_A3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B1_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B2_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_B3_6_well_plate_1.setStyleSheet("background-color: {}".format(color.name()))
            if self.plate_6_well is not None:
                for r in range(1, len(self.plate_6_well.ty)):
                    for c in range(1, len(self.plate_6_well.tx)):
                        mouvement = Mouvement(self.plate_6_well.tx[c], self.plate_6_well.ty[r], self.plate_6_well.A1_z,
                                              self.arduino)
                        # mouvement.toDo()
                        self.protocol.add_data(mouvement)
        else:
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

    def startThread(self):
        if self.lineEdit_number_repetition.text() == "":
            self.lineEdit_number_repetition.setText("1")

            if self.lineEdit_protocol_times_repetitions.text() == "":
                self.lineEdit_protocol_times_repetitions.setText("0")

            self.protocol.set_number_repetition(int(self.lineEdit_number_repetition.text()))
            self.protocol.set_time(int(self.lineEdit_protocol_times_repetitions.text()))

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
