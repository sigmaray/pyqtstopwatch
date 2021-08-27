import sys
from munch import Munch, munchify, unmunchify

from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QDialog,
    QCheckBox,
    QMessageBox
)

from PyQt5 import QtCore

import random

class TimeEndedDialog(QDialog):
    settings = None
    COLORS = ["white", "red"]
    colorIndex = 0

    def genStyle(self, color):
        return "background-color: " + color + ";"

    def onTimer(self):
        # print('l23')
        # color = random.choice(self.COLORS)
        if self.colorIndex == 0:
            self.colorIndex = 1
        else:
            self.colorIndex = 0
        color = self.COLORS[self.colorIndex]

        self.setStyleSheet(self.genStyle(color))

    def __init__(self):
        super().__init__()


        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # self.setModal(True)        
        self.setWindowTitle("Time Ended")
        # self.resize(270, 110)
        # Create a QFormLayout instance
        dlgLayout = QVBoxLayout()

        # formLayout = QFormLayout()
        # self.elIntervalMilliseconds = QLineEdit()
        # self.elIntervalMilliseconds.setText(str(existingSettings.intervalMilliseconds))
        # formLayout.addRow("Interval (milliseconds) (> 0):",
        #                   self.elIntervalMilliseconds)
        # self.elCellNum = QLineEdit()
        # self.elCellNum.setText(str(existingSettings.cellNum))
        # formLayout.addRow("Cell Num (>= 2):", self.elCellNum)
        # self.elCheckIsOut = QCheckBox()
        # self.elCheckIsOut.setChecked(existingSettings.checkIsOut)
        # formLayout.addRow("Check is Out", self.elCheckIsOut)
        # self.elCheckIsColliding = QCheckBox()
        # self.elCheckIsColliding.setChecked(existingSettings.checkIsColliding)
        # formLayout.addRow("Check is Colliding", self.elCheckIsColliding)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(
            # QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            QDialogButtonBox.Ok
        )

        self.button_box.accepted.connect(self.onAccept)
        # self.button_box.accepted.connect(self.accept)
        # self.button_box.rejected.connect(self.onReject)

        self.onTimer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(300)

        dlgLayout.addWidget(QLabel("Time ended!"))

        # dlgLayout.addLayout(formLayout)
        # dlgLayout.addWidget(QLabel("Clicking Ok button will reset game progress and restart the application"))
        dlgLayout.addWidget(self.button_box)

        # Set the layout on the application's window
        self.setLayout(dlgLayout)

    def onAccept(self):
        # try:
        #     settings = Munch()
        #     settings.intervalMilliseconds = int(
        #         self.elIntervalMilliseconds.text())
        #     settings.cellNum = int(self.elCellNum.text())
        #     settings.checkIsOut = self.elCheckIsOut.isChecked()
        #     settings.checkIsColliding = self.elCheckIsColliding.isChecked()            
        #     if (validateSettings(settings)):
        #         self.settings = settings
        #         self.accept()
        #     else:
        #         raise ValueError
        # except ValueError:
        #     self.showWarning()
        self.accept()

    # def onReject(self):
    #     self.reject()

    @staticmethod
    def run():
        # dialog = SettingsDialog(parent)
        dialog = TimeEndedDialog()
        
        result = dialog.exec_()
        # date = dialog.dateTime()
        # return (date.date(), date.time(), result == QDialog.Accepted)
        # settings = None
        # return result == QDialog.Accepted)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = TimeEndedDialog()
    dlg.show()
    sys.exit(app.exec_())
