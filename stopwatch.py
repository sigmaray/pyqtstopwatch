# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import datetime
import sys
import lib


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

        self.moveWindowToCenter()

        self.setFixedSize(self.size())

        # showing all the widgets
        self.show()

    def setIcon(self, str="--"):
        self.tray.setIcon(lib.drawIcon(str, "#FFFF00", "#6495ED"))

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

        self.tray.activated.connect(self.onTrayIconActivated)

        self.tray.setVisible(True)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            # if self.windowState() == QtCore.Qt.WindowMinimized:
            self.setWindowState(QtCore.Qt.WindowActive)
            self.activateWindow()

    def moveWindowToCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def uiComponents(self):
        self.addTrayIcon()

        self.label = QLabel(self)
        self.label.setGeometry(75, 100, 250, 70)
        self.label.setStyleSheet("border : 4px solid black;")
        self.label.setText("--")

        # setting font to the label
        self.label.setFont(QFont('Arial', 25))

        # setting alignment to the text of label
        self.label.setAlignment(Qt.AlignCenter)

        start_button = QPushButton("Start", self)
        start_button.setGeometry(125, 250, 150, 40)
        start_button.pressed.connect(self.start)

        pause_button = QPushButton("Pause", self)
        pause_button.setGeometry(125, 300, 150, 40)
        pause_button.pressed.connect(self.pause)


        reset_button = QPushButton("Re-set", self)
        reset_button.setGeometry(125, 350, 150, 40)
        reset_button.pressed.connect(self.reset)

        minimize_button = QPushButton("Minimize to tray", self)
        minimize_button.setGeometry(125, 400, 150, 40)
        minimize_button.pressed.connect(self.hide)

        # creating a timer object
        timer = QTimer(self)
        timer.timeout.connect(self.timeLoop)
        timer.start(100)

    def updateTexts(self):
        if self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.label.setText(text)
            if not self.isPaused:
                self.setIcon(lib.genTextShort(self.count))
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
