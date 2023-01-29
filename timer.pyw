import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from timerEndedDialog import TimeEndedDialog
import lib
import parseString

class Window(QMainWindow):
    COLOR1 = "#fff"
    # COLOR2 = "#000080"
    COLOR2 = "#000"

    chosenInterval = 0
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
        # actionQuit.triggered.connect(qApp.quit)
        actionQuit.triggered.connect(self.areYouSureAndClose)

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
            # self.show()
            # # if self.windowState() == QtCore.Qt.WindowMinimized:
            # self.setWindowState(QtCore.Qt.WindowActive)
            # self.activateWindow()

            if self.isHidden():
                self.show()
            else:
                self.hide()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.onClickStartPause()

    def moveWindowToCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def __init__(self):
        super().__init__()

        if lib.instance_already_running('timer'):
            print('Another instance is already running. Exiting')
            sys.exit()

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # self.setWindowIcon(QtGui.QIcon('images.png'))
        self.setWindowIcon(QtGui.QIcon(lib.get_current_directory() + "/" + 'images.png'))

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
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.buttonSet = QPushButton("Set time(s)", self)
        # self.buttonSet.setGeometry(125, 50, 150, 50)
        self.buttonSet.clicked.connect(self.onClickSet)

        self.layout.addWidget(self.buttonSet)

        self.buttonSetStart = QPushButton("Set time and start", self)
        # buttonSetStart.setGeometry(125, 50, 150, 50)
        self.buttonSetStart.clicked.connect(self.onClickSetStart)

        self.layout.addWidget(self.buttonSetStart)

        self.labelTimeSet = QLabel("time set: --", self)
        # self.labelTimeSet.setGeometry(100, 140, 200, 50)
        self.labelTimeSet.setStyleSheet("border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        self.labelTimeSet.setFont(QFont('Times', 15))
        self.labelTimeSet.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.labelTimeSet)

        self.labelCountdown = QLabel("countdown: --", self)
        # self.labelCountdown.setGeometry(100, 140, 200, 50)
        self.labelCountdown.setStyleSheet("border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        self.labelCountdown.setFont(QFont('Times', 15))
        self.labelCountdown.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.labelCountdown)

        self.buttonStartPause = QPushButton("Start", self)
        # self.buttonStartPause.setGeometry(125, 230, 150, 50)
        self.buttonStartPause.clicked.connect(self.onClickStartPause)
        self.buttonStartPause.setDisabled(True)

        self.layout.addWidget(self.buttonStartPause)

        self.buttonReset = QPushButton("Reset", self)
        # self.buttonReset.setGeometry(125, 300, 150, 50)
        self.buttonReset.clicked.connect(self.onClickReset)
        self.buttonReset.setDisabled(True)

        self.layout.addWidget(self.buttonReset)

        self.buttonMinimize = QPushButton("Hide to tray", self)
        # self.buttonMinimize.setGeometry(125, 440, 150, 50)
        self.buttonMinimize.pressed.connect(self.hide)

        self.layout.addWidget(self.buttonMinimize)

        # self.buttonExit = QPushButton("Exit (not to tray)", self)
        # self.buttonExit.setGeometry(125, 500, 150, 40)
        # self.buttonExit.clicked.connect(self.areYouSureAndClose)
        # self.layout.addWidget(self.buttonExit)

        # self.check_box = QCheckBox('Close to Tray')
        # self.layout.addWidget(self.check_box)
        # self.layout.addWidget(self.buttonMinimize)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
    
    def areYouSureAndClose(self):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()        

    def onTimer(self):
        if self.isRunning and not self.isPaused:
            self.count -= 1

            if self.count == 0:
                self.isRunning = False
                self.updateTexts(True)
                # TimeEndedDialog.run(self)
                TimeEndedDialog.run()
                self.updateTexts()
                self.buttonStartPause.setText('Start')
                # self.buttonStartPause.setDisabled(True)
                self.buttonReset.setDisabled(True)

        if self.isRunning:
            self.updateTexts()

    def updateTexts(self, completed=False):
        if completed:
            self.labelCountdown.setText("Completed !!!! ")
            self.setTrayText("!!!")
        elif self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.labelCountdown.setText("countdown: " + text)
            if not self.isPaused:
                self.setTrayText(lib.genTextShort(self.count))
            else:
                self.setTrayText("p")
        else:
            self.setTrayText("--")
            self.labelCountdown.setText("countdown: --")

        if self.chosenInterval > 0:
            self.labelTimeSet.setText("time set: " + lib.genTextFull(self.chosenInterval))

    def parseInputtedValue(self, value):
        if not parseString.isStringValid(value):
            return 0
        else:
            w = parseString.withoutQualifier(value)
            m = parseString.getQualifierMult(value)
            return w * m

    def askTime(self):
        second, done = QInputDialog.getText(self, 'Seconds', 'Enter Seconds:')
        v = self.parseInputtedValue(second)
        return v, done

    def onClickSet(self):
        v, done = self.askTime()

        if done and v > 0:
            self.chosenInterval = v * 10

            self.isRunning = False
            self.isPaused = False

            self.buttonStartPause.setText("Start")
            self.buttonStartPause.setDisabled(False)
            self.buttonReset.setDisabled(True)

            self.updateTexts()

    def onClickSetStart(self):
        v, done = self.askTime()

        if done and v > 0:
            self.chosenInterval = self.count = v * 10

            self.isRunning = True
            self.isPaused = False

            self.buttonStartPause.setText("Pause")
            self.buttonStartPause.setDisabled(False)
            self.buttonReset.setDisabled(False)

            self.updateTexts()            

    def onClickStartPause(self):
        if self.count == 0 and not(self.isPaused) and not (self.chosenInterval == 0):
            # self.isRunning = False
            self.isRunning = True
            self.count = self.chosenInterval
            self.buttonStartPause.setText("Pause")
            self.buttonReset.setDisabled(False)
        else:            
            if not(self.isPaused):
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

        # self.buttonStartPause.setDisabled(True)
        self.buttonStartPause.setText('Start')
        self.buttonReset.setDisabled(True)

    def closeEvent(self, event):
        event.ignore()
        # if self.check_box.isChecked():
        #     # event.ignore()
        #     self.hide()
        # else:
        #     self.areYouSureAndClose()
        self.areYouSureAndClose()


App = QApplication(sys.argv)
App.setQuitOnLastWindowClosed(False)
window = Window()
sys.exit(App.exec())
