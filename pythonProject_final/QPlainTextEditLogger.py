import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import pyqtSlot
from io import StringIO


class QPlainTextEditLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insertPlainText(message)

    def flush(self):
        pass
