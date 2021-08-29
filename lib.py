from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime

def drawIcon(str="--", textColor = "#000", bgColor = "#fff"):
    pixmap = QPixmap(24, 24)
    pixmap.fill(QColor(bgColor))

    painter = QPainter(pixmap)
    painter.setPen(QColor(textColor))
    painter.setFont(QFont('Arial', 10))
    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str)
    painter.end()
    return QIcon(pixmap)

def genTextFull(count):
    tdShort = datetime.timedelta(seconds=round(count/10))
    tdFull = datetime.timedelta(seconds=count/10)
    mStr = str(round(tdFull.microseconds / 100000))
    return str(tdShort) + "." + mStr

def genTextShort(count):
    seconds = count / 10
    secondsInt = round(seconds)
    minInt = round(seconds / 60)
    hFloat = float(seconds) / 60 / 60
    hInt = round(seconds / 60 / 60)
    if seconds <= 99:
        return str(secondsInt) + "s"
    elif minInt < 60:
        return str(minInt) + "m"
    elif minInt >= 60 and hInt < 10:
        return str(round(hFloat, 1)) + "h"
    elif hInt >= 10:
        return str(hInt) + "h"