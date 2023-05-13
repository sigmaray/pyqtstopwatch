"""Dialog telling user that time is over (used in timer.pyw)"""
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore


class TimeEndedDialog(QDialog):
    """Dialog that tells user that time is over (used in timer.pyw)"""

    # Background colors of dialog (the)
    COLORS = ["white", "red"]

    # Current background color index
    colorIndex = 0

    # def __init__(self, parent):
    def __init__(self):
        super().__init__()

        # self.setModal(True)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Time Ended")

        dlgLayout = QVBoxLayout()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(400)

        dlgLayout.addWidget(QLabel("Time ended!"))

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        dlgLayout.addWidget(self.button_box)

        self.setLayout(dlgLayout)

    def genStyle(self, color):
        """Generate CSS stylesheet that changes window background color"""
        return "background-color: " + color + ";"

    def onTimer(self):
        """
        When timer is triggered: change background color
        """
        if self.colorIndex == 0:
            self.colorIndex = 1
        else:
            self.colorIndex = 0
        color = self.COLORS[self.colorIndex]

        self.setStyleSheet(self.genStyle(color))

    @staticmethod
    def run():
        """Create and show dialog"""
        dialog = TimeEndedDialog()
        dialog.exec_()

# If this file is launched (instead of including) render dialog (for development purposes)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = TimeEndedDialog()
    dlg.show()
    sys.exit(app.exec_())
