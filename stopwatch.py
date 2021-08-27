# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import datetime
import sys


class Window(QMainWindow):
    count = 0
    isRunning = False
    isPaused = False

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("PStopwatch")

        # setting geometry
        self.setGeometry(100, 100, 400, 500)

        # calling method
        self.uiComponents()

        # showing all the widgets
        self.show()

    def genTextFull(self):
        tdShort = datetime.timedelta(seconds=round(self.count/10))
        tdFull = datetime.timedelta(seconds=self.count/10)
        m = tdFull.microseconds
        mStr = str(round(tdFull.microseconds / 100000))
        return str(tdShort) + "." + mStr

    def genTextShort(self):
        seconds = self.count / 10
        secondsInt = round(seconds)
        minInt = round(seconds / 60)
        hFloat = float(seconds) / 60 / 60
        hInt = round(seconds / 60 / 60)
        if seconds <= 99:
            return str(secondsInt) + "s"
        elif minInt < 10:
            return str(round(seconds / 60, 1)) + "m"
        elif minInt >= 10 and minInt < 60:
            return str(minInt) + "m"
        elif minInt >= 60 and hInt < 10:
            return str(round(hFloat, 1)) + "h"
        elif hInt >= 10:
            return str(hInt) + "h"

    def drawIconText(self, str="--"):
        pixmap = QPixmap(24, 24)
        pixmap.fill(QColorConstants.Svg.cornflowerblue)
        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 9))
        painter.setPen(QColor("#FFFF00"))
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str)
        painter.end()
        return QIcon(pixmap)

    def setIcon(self, str="--"):
        self.tray.setIcon(self.drawIconText(str))

    def addTrayIcon(self):
        self.tray = QSystemTrayIcon()

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray.setContextMenu(tray_menu)

        self.setIcon("--")

        # self.tray.activated.connect(self.onTrayIconActivated)

        # self.tray.setToolTip("Hi!")
        self.tray.setVisible(True)

    def uiComponents(self):
        self.addTrayIcon()
        # creating a label to show the time
        self.label = QLabel(self)

        # setting geometry of label
        self.label.setGeometry(75, 100, 250, 70)

        # adding border to the label
        self.label.setStyleSheet("border : 4px solid black;")

        # setting text to the label
        # self.label.setText(str(self.count))
        self.label.setText("--")

        # setting font to the label
        self.label.setFont(QFont('Arial', 25))

        # setting alignment to the text of label
        self.label.setAlignment(Qt.AlignCenter)

        # creating start button
        start = QPushButton("Start", self)

        # setting geometry to the button
        start.setGeometry(125, 250, 150, 40)

        # add action to the method
        start.pressed.connect(self.start)

        # creating pause button
        pause = QPushButton("Pause", self)

        # setting geometry to the button
        pause.setGeometry(125, 300, 150, 40)

        # add action to the method
        pause.pressed.connect(self.pause)

        # creating reset button
        re_set = QPushButton("Re-set", self)

        # setting geometry to the button
        re_set.setGeometry(125, 350, 150, 40)

        # add action to the method
        re_set.pressed.connect(self.reset)

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.timeLoop)

        # update the timer every tenth second
        timer.start(100)

    def updateTexts(self):
        if self.isRunning:
            text = self.genTextFull()
            if self.isPaused:
                text += " paused"
            self.label.setText(text)
            if not self.isPaused:
                self.setIcon(self.genTextShort())
            else:
                self.setIcon("p")
        else:
            self.setIcon("--")
            self.label.setText("--")
        

    # method called by timer
    def timeLoop(self):

        # checking if flag is true
        if self.isRunning and not(self.isPaused):
            # incrementing the counter
            self.count += 1

        self.updateTexts()

    def start(self):

        # making flag to true
        self.isRunning = True
        self.isPaused = False

    def pause(self):
        self.isPaused = True

        self.updateTexts()

    def reset(self):
        self.isRunning = False
        self.isPaused = False

        # reseeting the count
        self.count = 0

        # setting text to label
        self.updateTexts()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
