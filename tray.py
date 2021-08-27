
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Adding an icon
# icon = QIcon("icon.png")
icon = QIcon()


pixmap = QPixmap(24, 24)
pixmap.fill(QtCore.Qt.white)
painter = QPainter(pixmap)
# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Hi!")
painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "hello")
# painter.end()
icon = QIcon(pixmap);
tray = QSystemTrayIcon()

tray.setIcon(icon)
tray.setToolTip("Hi!")
tray.setVisible(True)

# Adding item on the menu bar
# tray = QSystemTrayIcon()
# tray.setIcon(icon)
# tray.setVisible(True)

# Creating the options
menu = QMenu()
option1 = QAction("Geeks for Geeks")
option2 = QAction("GFG")
menu.addAction(option1)
menu.addAction(option2)

# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)

app.exec_()
