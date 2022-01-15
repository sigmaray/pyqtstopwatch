import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants

import lib


class Window(QMainWindow):
    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    count = 0
    isRunning = False
    isPaused = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PythonChimes")

        self.setGeometry(100, 100, 400, 500)

        self.uiComponents()

        self.moveWindowToCenter()

        self.setFixedSize(self.size())

        # self.addTimer()

        self.show()

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
        # if reason == QSystemTrayIcon.DoubleClick:
        if reason == QSystemTrayIcon.Trigger:
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

        # self.label = QLabel(self)
        # self.label.setGeometry(75, 100, 250, 70)
        # self.label.setStyleSheet(
        #     "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        # self.label.setText("--")
        # self.label.setFont(QFont('Arial', 25))
        # self.label.setAlignment(Qt.AlignCenter)

        # self.buttonStartPause = QPushButton("Start", self)
        # self.buttonStartPause.setGeometry(125, 250, 150, 40)
        # self.buttonStartPause.pressed.connect(self.onClickStartPause)

        # self.buttonReset = QPushButton("Reset", self)
        # self.buttonReset.setGeometry(125, 325, 150, 40)
        # self.buttonReset.pressed.connect(self.onClickReset)
        # self.buttonReset.setDisabled(True)

        # buttonMinimize = QPushButton("Minimize to tray", self)
        # buttonMinimize.setGeometry(125, 425, 150, 40)
        # buttonMinimize.pressed.connect(self.hide)

        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.b1 = QCheckBox("Chimes at xx:30 minutes")
        # self.b1.setChecked(True)
        self.b1.stateChanged.connect(lambda:self.onb1change(self.b1))
        self.layout.addWidget(self.b1)

        self.b2 = QCheckBox("Chimes every xx:00 minutes")
        # self.b2.setChecked(True)
        self.b2.stateChanged.connect(lambda:self.onb2change(self.b2))
        self.layout.addWidget(self.b2)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        
        # self.setLayout(self.layout)

    def onb1change(self,b1):
        if b1.isChecked() == True:
           print(b1.text()+" is selected")
        else:
           print(b1.text()+" is deselected")

    def onb2change(self,b2):
        if b2.isChecked() == True:
           print(b2.text()+" is selected")
        else:
           print(b2.text()+" is deselected")

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

        self.count = 0

        self.updateTexts()

        self.buttonStartPause.setText("Start")

        self.buttonReset.setDisabled(True)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
