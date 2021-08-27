# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from time_ended_dialog import TimeEndedDialog


def genText(seconds):
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


class Window(QMainWindow):

	def drawIcon(self, str="--"):
		icon = QIcon()
		pixmap = QPixmap(24, 24)
		pixmap.fill(QtCore.Qt.white)
		painter = QPainter(pixmap)
		# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Hi!")
		# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "hello")
		painter.setFont(QFont('Arial', 9))
		# s = 40
		# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, genText(s))
		painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str)
		painter.end()
		return QIcon(pixmap)

	def setIcon(self, str="--"):
		self.tray.setIcon(self.drawIcon(str))

	def addTrayIcon(self):
		# Adding an icon
		# icon = QIcon("icon.png")

		self.tray = QSystemTrayIcon()

		# Creating the options
		menu = QMenu()
		option1 = QAction("Geeks for Geeks")
		option2 = QAction("GFG")
		menu.addAction(option1)
		menu.addAction(option2)

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

		# Adding options to the System Tray
		# self.tray.setContextMenu(menu)
		self.tray.setToolTip("Hi!")
		self.tray.setVisible(True)

	def onTrayIconActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.show()
			# if self.windowState() == QtCore.Qt.WindowMinimized:
			self.setWindowState(QtCore.Qt.WindowActive)
			self.activateWindow()

	def __init__(self):
		super().__init__()

		# self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

		# setting title
		self.setWindowTitle("PTimer")

		# setting geometry
		self.setGeometry(100, 100, 400, 600)

		# calling method
		self.UiComponents()

		self.addTrayIcon()

		# showing all the widgets
		self.show()

	# method for widgets
	def UiComponents(self):

		# variables
		# count variable
		self.count = 0

		# start flag
		self.start = False

		# creating push button to get time in seconds
		button = QPushButton("Set time(s)", self)

		# setting geometry to the push button
		button.setGeometry(125, 100, 150, 50)

		# adding action to the button
		button.clicked.connect(self.get_seconds)

		# creating push button to get time in seconds
		buttonS = QPushButton("Set time(s) and start", self)

		# setting geometry to the push button
		buttonS.setGeometry(125, 160, 150, 50)

		# adding action to the button
		buttonS.clicked.connect(self.get_seconds_and_start)

		# creating label to show the seconds
		# self.label = QLabel("//TIMER//", self)
		self.label = QLabel("--", self)

		# setting geometry of label
		self.label.setGeometry(100, 250, 200, 50)

		# setting border to the label
		self.label.setStyleSheet("border : 3px solid black")

		# setting font to the label
		self.label.setFont(QFont('Times', 15))

		# setting alignment ot the label
		self.label.setAlignment(Qt.AlignCenter)

		# creating start button
		start_button = QPushButton("Start", self)

		# setting geometry to the button
		start_button.setGeometry(125, 350, 150, 40)

		# adding action to the button
		start_button.clicked.connect(self.start_action)



		# creating reset button
		reset_button = QPushButton("Reset", self)

		# setting geometry to the button
		reset_button.setGeometry(125, 400, 150, 40)

		# adding action to the button
		reset_button.clicked.connect(self.reset_action)

				# creating pause button
		pause_button = QPushButton("Pause", self)

		# setting geometry to the button
		pause_button.setGeometry(125, 450, 150, 40)

		# adding action to the button
		pause_button.clicked.connect(self.pause_action)

		# creating pause button
		exit_button = QPushButton("Exit", self)

		# setting geometry to the button
		exit_button.setGeometry(125, 500, 150, 40)

		exit_button.clicked.connect(qApp.quit)

		self.check_box = QCheckBox('Minimize to Tray on Close', self)
		self.check_box.setGeometry(125, 550, 250, 40)
		self.check_box.setChecked(True)

		# creating a timer object
		timer = QTimer(self)

		# adding action to timer
		timer.timeout.connect(self.showTime)

		# update the timer every tenth second
		timer.start(100)

	def closeEvent(self, event):
		if self.check_box.isChecked():
			event.ignore()
			self.hide()
			# self.tray_icon.showMessage(
			# 	"Tray Program",
			# 	"Application was minimized to Tray",
			# 	QSystemTrayIcon.Information,
			# 	2000
			# )

	# method called by timer
	def showTime(self):

		# checking if flag is true
		if self.start:
			# incrementing the counter
			self.count -= 1

			# timer is completed
			if self.count == 0:

				# making flag false
				self.start = False

				# setting text to the label
				self.label.setText("Completed !!!! ")
				self.setIcon("!")

				TimeEndedDialog.run()

				self.setIcon("--")
				self.label.setText("--")

		if self.start:
			# getting text from count
			text = str(self.count / 10) + " s"

			# showing text
			self.label.setText(text)
			self.setIcon(genText(self.count / 10))

	# method called by the push button

	def get_seconds(self):

		# making flag false
		self.start = False

		# getting seconds and flag
		second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

		# if flag is true
		if done:
			# changing the value of count
			self.count = second * 10

			# setting text to the label
			self.label.setText(str(second))

	# method called by the push button
	def get_seconds_and_start(self):

		# making flag false
		self.start = False

		# getting seconds and flag
		second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

		# if flag is true
		if done and second > 0:
			# changing the value of count
			self.count = second * 10

			# setting text to the label
			self.label.setText(str(second))

			self.start_action()

	def start_action(self):
		if self.count == 0:
			self.start = False
		else:
			# making flag true
			self.start = True
			self.label.setText(genText(self.count / 10))

		# count = 0
		
			

	def pause_action(self):
		if self.start:
			# self.setIcon("paused")
			self.label.setText(str(self.count / 10) + "s" + " " + "paused")
			self.setIcon("p")
			# making flag false
			self.start = False

	def reset_action(self):

		# making flag false
		self.start = False

		# setting count value to 0
		self.count = 0

		# setting label text
		# self.label.setText("//TIMER//")
		self.label.setText("--")

		self.label.setText("--")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
