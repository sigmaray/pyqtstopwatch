
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

def genText(seconds):
    minInt = round(seconds / 60)
    hFloat  = float(seconds) / 60 / 60
    hInt = round(seconds / 60 / 60)
    if seconds <= 99:
        return str(seconds) + "s"
    elif minInt < 10 :
        return str(round(float(seconds) / 60, 1)) + "m"
    elif minInt >= 10 and minInt < 60:
        return str(minInt) + "m"
    elif minInt >= 60 and hInt < 10:
        return str(round(hFloat, 1)) + "h"
    elif hInt >= 10:
        return str(hInt) + "h"

# Adding an icon
# icon = QIcon("icon.png")
icon = QIcon()


pixmap = QPixmap(24, 24)
pixmap.fill(QtCore.Qt.white)
painter = QPainter(pixmap)
# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Hi!")
# painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "hello")
s = 40
painter.setFont(QFont('Arial', 9))
painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, genText(s))
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
