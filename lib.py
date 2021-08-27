from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

def drawIcon(str="--"):
    pixmap = QPixmap(24, 24)
    pixmap.fill(QtCore.Qt.white)
    painter = QPainter(pixmap)
    painter.setFont(QFont('Arial', 9))
    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str)
    painter.end()
    return QIcon(pixmap)
