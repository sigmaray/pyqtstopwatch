import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class TimeEndedDialog(QDialog):
    COLORS = ["white", "red"]
    colorIndex = 0

    def genStyle(self, color):
        return "background-color: " + color + ";"

    def onTimer(self):
        if self.colorIndex == 0:
            self.colorIndex = 1
        else:
            self.colorIndex = 0
        color = self.COLORS[self.colorIndex]

        self.setStyleSheet(self.genStyle(color))

    def __init__(self):
        super().__init__()

        # self.setModal(True)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Time Ended")

        dlgLayout = QVBoxLayout()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(400)

        dlgLayout.addWidget(QLabel("Time ended!"))

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        dlgLayout.addWidget(self.button_box)

        self.setLayout(dlgLayout)

    @staticmethod
    def run():
        dialog = TimeEndedDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = TimeEndedDialog()
    dlg.show()
    sys.exit(app.exec_())
