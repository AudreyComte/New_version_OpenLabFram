from PyQt5 import QtWidgets
import sys
from arduino import Arduino

from event import Event2
from mainwindow import Ui_OpenLabFrame

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     OpenLabFrame = QtWidgets.QWidget()
#     ui = Ui_OpenLabFrame()
#     ui.setupUi(OpenLabFrame)
#     OpenLabFrame.show()
#     sys.exit(app.exec_())
#
#

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fenetre = QtWidgets.QMainWindow()
    ui = Event2(fenetre)
    fenetre.show()
    app.exec_()

