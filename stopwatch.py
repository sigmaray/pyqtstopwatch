import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import lib


class Window(QMainWindow):
    count = 0
    isRunning = False
    isPaused = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PythonStopwatch")

        self.setGeometry(100, 100, 400, 500)

        self.uiComponents()

        self.moveWindowToCenter()

        self.setFixedSize(self.size())

        self.addTimer()

        self.show()

    def setTrayText(self, str="--"):
        self.tray.setIcon(lib.drawIcon(str, "#FFFF00", "#6495ED"))

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

    def uiComponents(self):
        self.addTrayIcon()

        self.label = QLabel(self)
        self.label.setGeometry(75, 100, 250, 70)
        self.label.setStyleSheet("border : 4px solid black;")
        self.label.setText("--")
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter)

        buttonStart = QPushButton("Start", self)
        buttonStart.setGeometry(125, 250, 150, 40)
        buttonStart.pressed.connect(self.onClickStart)

        buttonPause = QPushButton("Pause", self)
        buttonPause.setGeometry(125, 300, 150, 40)
        buttonPause.pressed.connect(self.onClickPause)

        buttonReset = QPushButton("Re-set", self)
        buttonReset.setGeometry(125, 350, 150, 40)
        buttonReset.pressed.connect(self.onClickReset)

        buttonMinimize = QPushButton("Minimize to tray", self)
        buttonMinimize.setGeometry(125, 400, 150, 40)
        buttonMinimize.pressed.connect(self.hide)

    def addTimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def updateTexts(self):
        if self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.label.setText(text)
            if not self.isPaused:
                self.setTrayText(lib.genTextShort(self.count))
            else:
                self.setTrayText("p")
        else:
            self.setTrayText("--")
            self.label.setText("--")

    def onTimer(self):
        if self.isRunning and not(self.isPaused):
            self.count += 1

        self.updateTexts()

    def onClickStart(self):
        self.isRunning = True
        self.isPaused = False

    def onClickPause(self):
        self.isPaused = True

        self.updateTexts()

    def onClickReset(self):
        self.isRunning = False
        self.isPaused = False

        self.count = 0

        self.updateTexts()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
