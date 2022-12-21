import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
from munch import munchify
import os

import lib

class Window(QMainWindow):
    COLOR1 = "#fff"
    # COLOR2 = "#6495ED"
    COLOR2 = "#000"

    count = 0
    isRunning = False
    isPaused = False

    def __init__(self):
        super().__init__()

        self.settings = munchify(lib.readWriteSettings())
        self.count = self.settings.count
        if self.count > 0:
            self.isRunning = True
            self.isPaused = True

        if lib.instance_already_running():
            print('Another instance is already running. Exiting')
            sys.exit()

        self.setWindowTitle("PythonStopwatch")

        self.setGeometry(100, 100, 400, 500)

        self.uiComponents()

        self.moveWindowToCenter()

        self.setFixedSize(self.size())

        self.addTimer()

        self.show()

    def setTrayText(self, str="--"):
        self.tray.setIcon(lib.drawIcon(str, self.COLOR1, self.COLOR2))

    def addTrayIcon(self):
        self.tray = QSystemTrayIcon()

        actionStartPause = QAction("Start/Pause", self)
        actionReset = QAction("Reset", self)
        actionHide = QAction("Hide", self)        
        actionShow = QAction("Show", self)
        actionQuit = QAction("Exit", self)
        actionHide = QAction("Hide", self)
        actionStartPause.triggered.connect(self.onClickStartPause)
        actionReset.triggered.connect(self.onClickReset)
        actionShow.triggered.connect(self.show)
        actionHide.triggered.connect(self.hide)
        actionQuit.triggered.connect(self.areYouSureAndClose)
        menu = QMenu()
        menu.addAction(actionStartPause)
        menu.addAction(actionReset)
        menu.addAction(actionShow)
        menu.addAction(actionHide)
        menu.addAction(actionQuit)
        self.tray.setContextMenu(menu)

        self.setTrayText("--")

        self.tray.activated.connect(self.onTrayIconActivated)

        self.tray.setVisible(True)

    def onTrayIconActivated(self, reason):
        # if reason == QSystemTrayIcon.DoubleClick:
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.hide()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.onClickStartPause()
            # # if self.windowState() == QtCore.Qt.WindowMinimized:
            # self.setWindowState(QtCore.Qt.WindowActive)
            # self.activateWindow()

    def moveWindowToCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def uiComponents(self):
        self.addTrayIcon()

        self.label = QLabel(self)
        self.label.setGeometry(75, 30, 250, 70) # yStart: 30, yEnd: 100, yDelta: 30
        self.label.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        
        # raise Exception(str(self.count))
        # if self.count != 0:
        #     self.setTrayText(lib.genTextShort(self.count))
        # else:
        #     self.label.setText("--")
        self.updateTexts()

        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter)

        self.buttonStartPause = QPushButton("Start", self)
        self.buttonStartPause.setGeometry(125, 150, 150, 40) # yStart: 150, yEnd: 190, yDelta: 50
        self.buttonStartPause.pressed.connect(self.onClickStartPause)

        self.buttonReset = QPushButton("Reset", self)
        self.buttonReset.setGeometry(125, 240, 150, 40) # yStart: 240, yEnd: 280, yDelta: 50
        self.buttonReset.pressed.connect(self.onClickReset)
        self.buttonReset.setDisabled(not self.isRunning)

        buttonMinus1h = QPushButton("-1h", self)
        buttonMinus1h.setGeometry(10, 330, 50, 40) # xStart: 130, xEnd: 160, xDelta: 10, yStart: 330, yEnd: 370, yDelta: 50
        buttonMinus1h.pressed.connect(self.onClickMinus1h)

        buttonMinus10m = QPushButton("-10m", self)
        buttonMinus10m.setGeometry(70, 330, 50, 40) # xStart: 70, xEnd: 120, xDelta: 10, yStart: 330, yEnd: 370, yDelta: 50
        buttonMinus10m.pressed.connect(self.onClickMinus10m)

        buttonMinus1m = QPushButton("-1m", self)
        buttonMinus1m.setGeometry(130, 330, 50, 40) # xStart: 10, xEnd: 60, xDelta: 10, yStart: 330, yEnd: 370, yDelta: 50
        buttonMinus1m.pressed.connect(self.onClickMinus1m)

        buttonPlus1m = QPushButton("+1m", self)
        buttonPlus1m.setGeometry(220, 330, 50, 40)
        buttonPlus1m.pressed.connect(self.onClickPlus1m)

        buttonPlus10m = QPushButton("+10m", self)
        buttonPlus10m.setGeometry(280, 330, 50, 40)
        buttonPlus10m.pressed.connect(self.onClickPlus10m)

        buttonPlus1h = QPushButton("+1h", self)
        buttonPlus1h.setGeometry(340, 330, 50, 40)
        buttonPlus1h.pressed.connect(self.onClickPlus1h)

        buttonMinimize = QPushButton("Minimize to tray", self)
        buttonMinimize.setGeometry(125, 420, 150, 40)
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
            self.changeTimeByDelta(1)
 
        # self.updateTexts()

    def onClickStartPause(self):
        if self.isRunning == False:
            self.isPaused = False
            self.isRunning = True
            self.buttonStartPause.setText("Pause")
            self.buttonReset.setDisabled(False)
        elif not(self.isPaused):
            self.isPaused = True
            self.buttonStartPause.setText("Start")
        elif self.isPaused:
            self.isPaused = False
            self.buttonStartPause.setText("Pause")

        self.updateTexts()

    def onClickReset(self):
        self.isRunning = False
        self.isPaused = False

        self.settings.count = self.count = 0
        lib.writeSettingsFile(self.settings)

        self.updateTexts()

        self.buttonStartPause.setText("Start")

        self.buttonReset.setDisabled(True)

    def changeTimeByDelta(self, delta):
        print("changeTime, delta: " + str(delta))        

        newVal = self.count + delta

        if newVal < 0 or not(self.isRunning):
            return

        self.settings.count = self.count = newVal

        # if self.count % 10 == 0:
        if True:
            lib.writeSettingsFile(self.settings)

        self.updateTexts()

    def onClickMinus1h(self):
        print("onClickMinus1h")        
        self.changeTimeByDelta(-60 * 10 * 60)

    def onClickMinus10m(self):
        print("onClickMinus10m")
        self.changeTimeByDelta(-60 * 10 * 10)

    def onClickMinus1m(self):
        print("onClickMinus1m")
        self.changeTimeByDelta(-60 * 10)

    def onClickPlus1m(self):
        print("onClickPlus1m")
        self.changeTimeByDelta(60 * 10)

    def onClickPlus10m(self):
        print("onClickPlus10m")
        self.changeTimeByDelta(60 * 10 * 10)

    def onClickPlus1h(self):
        print("onClickPlus1h")
        self.changeTimeByDelta(60 * 10 * 60)

    def closeEvent(self, event):
        event.ignore()    
        self.areYouSureAndClose()

    def areYouSureAndClose(self):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()    

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
