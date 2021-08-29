import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from timerEndedDialog import TimeEndedDialog
import lib


class Window(QMainWindow):
    COLOR1 = "#fff"
    COLOR2 = "#000080"

    count = 0
    isRunning = False
    isPaused = False

    def setTrayText(self, str="--"):
        self.tray.setIcon(lib.drawIcon(str, self.COLOR1, self.COLOR2))

    def addTrayIcon(self):
        self.tray = QSystemTrayIcon()

        actionShow = QAction("Show", self)
        actionQuit = QAction("Exit", self)
        actionHide = QAction("Hide", self)
        actionShow.triggered.connect(self.show)
        actionHide.triggered.connect(self.hide)
        actionQuit.triggered.connect(qApp.quit)

        menu = QMenu()
        menu.addAction(actionShow)
        menu.addAction(actionHide)
        menu.addAction(actionQuit)
        self.tray.setContextMenu(menu)

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

        self.setGeometry(100, 100, 400, 520)

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
        # buttonSet = QPushButton("Set time(s)", self)
        # buttonSet.setGeometry(125, 50, 150, 50)
        # buttonSet.clicked.connect(self.onClickSet)

        buttonSetStart = QPushButton("Set time and start", self)
        buttonSetStart.setGeometry(125, 50, 150, 50)
        buttonSetStart.clicked.connect(self.onClickSetStart)

        self.labelCountdown = QLabel("--", self)
        self.labelCountdown.setGeometry(100, 140, 200, 50)
        self.labelCountdown.setStyleSheet("border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        self.labelCountdown.setFont(QFont('Times', 15))
        self.labelCountdown.setAlignment(Qt.AlignCenter)

        buttonStart = QPushButton("Start", self)
        buttonStart.setGeometry(125, 230, 150, 50)
        buttonStart.clicked.connect(self.onClickStart)

        reset_button = QPushButton("Reset", self)
        reset_button.setGeometry(125, 300, 150, 50)
        reset_button.clicked.connect(self.onClickReset)

        buttonPause = QPushButton("Pause", self)
        buttonPause.setGeometry(125, 370, 150, 50)
        buttonPause.clicked.connect(self.onClickPause)

        buttonMinimize = QPushButton("Minimize to tray", self)
        buttonMinimize.setGeometry(125, 440, 150, 50)
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
