import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from time_ended_dialog import TimeEndedDialog
import lib


class Window(QMainWindow):
    count = 0
    isRunning = False
    isPaused = False

    def setTrayText(self, str="--"):
        self.tray.setIcon(lib.drawIcon(str, "#fff", "#000080"))

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

        self.setTrayText("--")

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

    def __init__(self):
        super().__init__()

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle("PythonTimer")

        self.setGeometry(100, 100, 400, 600)

        self.moveWindowToCenter()

        self.addUiComponents()

        self.addTimer()

        self.addTrayIcon()

        self.show()

    def addTimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def addUiComponents(self):
        buttonSet = QPushButton("Set time(s)", self)
        buttonSet.setGeometry(125, 50, 150, 50)
        buttonSet.clicked.connect(self.onClickSet)

        buttonSetStart = QPushButton("Set time(s) and start", self)
        buttonSetStart.setGeometry(125, 120, 150, 50)
        buttonSetStart.clicked.connect(self.onClickSetStart)

        self.labelCountdown = QLabel("--", self)
        self.labelCountdown.setGeometry(100, 200, 200, 50)
        self.labelCountdown.setStyleSheet("border : 3px solid black")
        self.labelCountdown.setFont(QFont('Times', 15))
        self.labelCountdown.setAlignment(Qt.AlignCenter)

        buttonStart = QPushButton("Start", self)
        buttonStart.setGeometry(125, 300, 150, 40)
        buttonStart.clicked.connect(self.onClickStart)
        reset_button = QPushButton("Reset", self)
        reset_button.setGeometry(125, 350, 150, 40)
        reset_button.clicked.connect(self.onClickReset)

        buttonPause = QPushButton("Pause", self)
        buttonPause.setGeometry(125, 400, 150, 40)
        buttonPause.clicked.connect(self.onClickPause)

        buttonMinimize = QPushButton("Minimize to tray", self)
        buttonMinimize.setGeometry(125, 450, 150, 40)
        buttonMinimize.pressed.connect(self.hide)

        # buttonExit = QPushButton("Exit", self)
        # buttonExit.setGeometry(125, 500, 150, 40)
        # buttonExit.clicked.connect(qApp.quit)

    def onTimer(self):
        if self.isRunning and not self.isPaused:
            self.count -= 1

            if self.count == 0:
                self.isRunning = False
                self.updateTexts(True)
                TimeEndedDialog.run()
                self.updateTexts()

        if self.isRunning:
            self.updateTexts()

    def updateTexts(self, completed=False):
        if completed:
            self.labelCountdown.setText("Completed !!!! ")
            self.setTrayText("!")
        elif self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.labelCountdown.setText(text)
            if not self.isPaused:
                self.setTrayText(lib.genTextShort(self.count))
            else:
                self.setTrayText("p")
        else:
            self.setTrayText("--")
            self.labelCountdown.setText("--")

    def onClickSet(self):
        self.isRunning = False

        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done:
            self.count = second * 10

            self.updateTexts()

    def onClickSetStart(self):
        self.onClickSet()
        self.onClickStart()

    def onClickStart(self):
        if self.count == 0:
            self.isRunning = False
        else:
            self.isRunning = True
            self.isPaused = False
            self.updateTexts()

    def onClickPause(self):
        if self.isRunning:
            self.isPaused = True
            self.updateTexts()

    def onClickReset(self):
        self.isRunning = False
        self.isPaused = False

        self.count = 0

        self.updateTexts()

    # def closeEvent(self, event):
    #     if self.check_box.isChecked():
    #         event.ignore()
    #         self.hide()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
