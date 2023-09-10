#!/usr/bin/python3
"""Stopwatch with tray icon implemented in PyQT"""
import sys
from munch import munchify, Munch
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5 import QtGui
from PyQt5.QtWidgets import qApp, QApplication, QAction, QMainWindow, QMessageBox, \
    QSystemTrayIcon, QMenu, QLabel, QPushButton, QDesktopWidget
import os

# Import modules from './include/' dir
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/include')
import helpers
from single_instance_windows import SingleInstanceWindows
from single_instance_unix import SingleInstanceUnix


class Stopwatch(QMainWindow, SingleInstanceUnix, SingleInstanceWindows):
    """
    Window of Stopwatch
    """

    SETTINGS_FILE = "stopwatch.json"

    # Color of text in tray icon
    COLOR1 = "#fff"

    # Background of tray icon, border and font color of label in the window
    COLOR2 = "#6495ED"

    state = Munch(
        counted=0,  # stopwatch interval in centiseconds
        currentCentiseconds=0,
        isRunning=False,
        isPaused=False
    )

    # Grouping all widgets into a single object/namespace
    widgets = Munch()

    def __init__(self):
        super().__init__()

        if self.isAlreadyRunningUnix() or self.isAlreadyRunningWindows():
            print('Another instance is already running. Exiting')
            QMessageBox.about(
                self, "Error", 'Another instance is already running. Exiting')
            sys.exit()

        self.loadStateFromDisk()

        self.setWindowTitle("PythonStopwatch")

        self.setGeometry(100, 100, 400, 500)

        self.setWindowIcon(QtGui.QIcon(
            helpers.getCurrentDirectory() + "/stopwatch/" + 'icon.png'))

        self.addUiComponents()

        self.moveWindowToCenter()

        self.setFixedSize(self.size())

        self.addTimer()

        self.show()

        self.updateTexts()

    def loadStateFromDisk(self):
        self.settings = munchify(helpers.readOrWriteSettings(
            self.SETTINGS_FILE, self.state))

        # When app is restarted stopwatch should not be started automatically
        if self.settings.isRunning and not self.settings.isPaused:
            self.settings.isPaused = True

        self.state.update(self.settings)

    def updateState(self, saveToDisk, **newValues):
        for key in newValues:
            self.settings[key] = self.state[key] = newValues[key]
        if saveToDisk:
            helpers.writeSettingsFile(self.SETTINGS_FILE, self.settings)

    def setTrayText(self, text="--"):
        """Render text in tray icon"""
        self.widgets.tray.setIcon(helpers.drawIcon(text, self.COLOR1, self.COLOR2))

    def addTrayIcon(self):
        """Add tray icon with menu"""
        self.widgets.tray = QSystemTrayIcon()  # pylint: disable=attribute-defined-outside-init

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
        actionQuit.triggered.connect(self.onExit)
        menu = QMenu()
        menu.addAction(actionStartPause)
        menu.addAction(actionReset)
        menu.addAction(actionShow)
        menu.addAction(actionHide)
        menu.addAction(actionQuit)
        self.widgets.tray.setContextMenu(menu)

        self.setTrayText("--")

        self.widgets.tray.activated.connect(self.onTrayIconActivated)

        self.widgets.tray.setVisible(True)

    def onTrayIconActivated(self, reason):
        """
        When tray icon is clicked:
        Show/Hide window if left mouse button is clicked
        Start/pause if middle mouse button is clicked
        """
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.hide()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.onClickStartPause()

    def moveWindowToCenter(self):
        """
        Center PyQt window
        https://pythonprogramminglanguage.com/pyqt5-center-window/
        """
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def addUiComponents(self):
        """Add UI components and connect them to handler functions"""
        self.addTrayIcon()

        self.widgets.label = QLabel(self)
        self.widgets.label.setGeometry(75, 30, 250, 70)
        self.widgets.label.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")

        self.widgets.label.setFont(QFont('Arial', 25))
        self.widgets.label.setAlignment(Qt.AlignCenter)

        self.widgets.buttonStartPause = QPushButton("Start", self)
        self.widgets.buttonStartPause.setGeometry(125, 150, 150, 40)
        self.widgets.buttonStartPause.pressed.connect(self.onClickStartPause)

        self.widgets.buttonReset = QPushButton("Reset", self)
        self.widgets.buttonReset.setGeometry(125, 240, 150, 40)
        self.widgets.buttonReset.pressed.connect(self.onClickReset)
        self.widgets.buttonReset.setDisabled(not self.state.isRunning)

        buttonMinus1h = QPushButton("-1h", self)
        buttonMinus1h.setGeometry(10, 330, 50, 40)
        buttonMinus1h.pressed.connect(self.onClickMinus1h)

        buttonMinus10m = QPushButton("-10m", self)
        buttonMinus10m.setGeometry(70, 330, 50, 40)
        buttonMinus10m.pressed.connect(self.onClickMinus10m)

        buttonMinus1m = QPushButton("-1m", self)
        buttonMinus1m.setGeometry(130, 330, 50, 40)
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
        """Add timer, connect it to handler function, start it"""
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        self.onTimer()

    def updateTexts(self):
        """Update texts in window and tray icon according to self.state"""
        if self.state.isRunning:
            text = '<html>'
            text += '&nbsp;&nbsp;&nbsp;'
            text += helpers.genTextFull(self.state.counted)
            if self.state.isPaused:
                text += " p"
            else:
                text += "&nbsp;&nbsp;&nbsp;"
            self.widgets.label.setText(text)
            text = '</html>'
            if not self.state.isPaused:
                self.setTrayText(helpers.genTextShort(self.state.counted))
            else:
                self.setTrayText("p")
        else:
            self.setTrayText("--")
            self.widgets.label.setText("--")

    def onTimer(self):
        """When timer is triggered: change time counter and update UI"""
        previousCentiseconds = self.state.currentCentiseconds or helpers.getCentiseconds()
        self.updateState(saveToDisk=False, currentCentiseconds=helpers.getCentiseconds())

        if self.state.isRunning and not self.state.isPaused:
            # Timer can be not accurate
            # https://stackoverflow.com/questions/58699630/accurate-timer-with-pyqt
            # self.updateState(saveToDisk=False, counted=self.state.counted + 1)
            delta = self.state.currentCentiseconds - previousCentiseconds
            self.updateState(saveToDisk=False, counted=self.state.counted + delta)
            self.updateTexts()

    def updateButtons(self):
        self.widgets.buttonReset.setDisabled(not self.state.isRunning)

        if self.state.isRunning:
            if self.state.isPaused:
                self.widgets.buttonStartPause.setText("Start")
            else:
                self.widgets.buttonStartPause.setText("Pause")
        else:
            self.widgets.buttonStartPause.setText("Start")
            self.widgets.buttonStartPause.setDisabled(False)

    def onClickStartPause(self):
        """
        When Start/Pause button is pressed
        * Update values in self.state
        * Change button text
        """
        if not self.state.isRunning:
            self.updateState(saveToDisk=True, isPaused=False, isRunning=True)
            self.updateButtons()
        elif not self.state.isPaused:
            self.updateState(saveToDisk=True, isPaused=True)
            self.updateButtons()
        else:
            self.updateState(saveToDisk=True, isPaused=False)
            self.updateButtons()

        self.updateTexts()

    def onClickReset(self):
        """
        When Reset button is pressed
        * Reset values in self.state
        * Update value in JSON settings file
        * Change text of Pause button to Start
        * Disable Reset button
        """
        self.updateState(saveToDisk=True, isRunning=False, isPaused=False, counted=0)

        self.updateTexts()

        self.updateButtons()

    def changeTimeByDeltaAndUpdateUI(self, delta):
        """
        Only if not paused:
        * Add (integer) delta to time counter.
        * Write new counter into JSON settings file.
        * Update UI (texts in window and tray icon)
        """
        newVal = self.state.counted + delta

        if newVal < 0 or not self.state.isRunning:
            return

        self.updateState(saveToDisk=True, counted=newVal)

        self.updateTexts()

    def onClickMinus1h(self):
        """When -1h button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(-60 * 60 * 100)

    def onClickMinus10m(self):
        """When -10m button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(-60 * 10 * 100)

    def onClickMinus1m(self):
        """When -1m button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(-60 * 100)

    def onClickPlus1m(self):
        """When +1m button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(60 * 100)

    def onClickPlus10m(self):
        """When +10m button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(60 * 10 * 100)

    def onClickPlus1h(self):
        """When +1h button is pressed"""
        self.changeTimeByDeltaAndUpdateUI(60 * 60 * 100)

    def closeEvent(self, event):
        """
        Overriding PyQt close event.
        Ask user's confirmation before exiting
        https://learndataanalysis.org/example-of-how-to-use-the-qwidget-close-event-pyqt5-tutorial/
        """
        event.ignore()
        self.onExit()

    def onExit(self):
        """
        Ask user's confirmation and exit
        """
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                     quit_msg, QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.updateState(saveToDisk=True)
            qApp.quit()


App = QApplication(sys.argv)
App.setQuitOnLastWindowClosed(False)
window = Stopwatch()
sys.exit(App.exec())
