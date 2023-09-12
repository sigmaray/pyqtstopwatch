"""Helper functions that are used in stopwatch.pyw and timer.pyw"""
import time
import datetime
import os
import json
import math
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont, QIcon
# from PyQt5.QtWidgets import QMessageBox

SETTINGS_FILE = "pyqtstopwatchd.json"


def getCentiseconds():
    """Get current time in centiseconds (since the epoch)"""
    return round(time.time() * 100)


def fullPath(fileName):
    """Append current directory (that contains script) to file name"""
    return getCurrentDirectory() + "/" + fileName


def doFileExist(fileName):
    """Check if file with fileName exists in current directory"""
    return os.path.isfile(fullPath(fileName))


def writeSettingsFile(fileName, hashmap):
    """Write hashmap into JSON file with fileName"""
    with open(file=fullPath(fileName), mode='w', encoding="utf-8") as f:
        f.write(json.dumps(hashmap))


def readSettingsFile(fileName):
    """Parse JSON file with fileName into a hashmap"""
    with open(file=fullPath(fileName), encoding="utf-8") as f:
        return json.load(f)


def readOrWriteSettings(settingsFilePath, defaultSettings):
    """
    Try to read settings.
    If settings file doesn't exist, create file with default values.
    If file exists and is not valid, exit.
    """
    if not doFileExist(settingsFilePath):
        print(settingsFilePath + " does not exist, creating it")
        writeSettingsFile(settingsFilePath, defaultSettings)

    settings = readSettingsFile(settingsFilePath)

    # if not validateSettings(settings, defaultSettings):
    #     QMessageBox.warning(None, "Error", settingsFilePath +
    #                       " is not valid. " +
    #                       "May be you are you using settings file from previous version " +
    #                       "of application and it has different format. " +
    #                       "You can delete it and restart the application. " +
    #                       "App will recreate settings file if it's not present")
    #     sys.exit()

    return settings


def validateSettings(settings, defaultSettings):
    """Validate hashmap with parsed settings. Ensure that all keys are present"""
    for key in defaultSettings.keys():
        if key not in settings.keys():  # or (type(settings[key]) != int) or (settings[key] < 0):
            return False

    return True


def drawIcon(strVal="--", textColor="#000", bgColor="#fff"):
    """Render string into QIcon to be shown in tray"""
    pixmap = QPixmap(24, 24)
    pixmap.fill(QColor(bgColor))

    painter = QPainter(pixmap)
    painter.setPen(QColor(textColor))

    if len(strVal) >= 3:
        fontSize = 10
    else:
        fontSize = 12
    painter.setFont(QFont('Arial', fontSize))

    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, strVal)
    painter.end()
    return QIcon(pixmap)


def genTextFull(count):
    """Convert int value into full time to be shown in window"""
    delta = datetime.timedelta(seconds=math.floor(count / 100))
    decisecond = str(count % 100)[0]
    return str(delta) + "." + decisecond


def genTextShort(count):
    """Convert int value into short time to be shown in tray"""
    seconds = count / 100
    secondsInt = math.floor(seconds)
    minInt = math.floor(seconds / 60)
    hFloat = float(seconds) / 60 / 60
    hInt = math.floor(seconds / 60 / 60)

    if seconds <= 99:
        return str(secondsInt) + "s"

    if minInt < 60:
        return str(minInt) + "m"

    if minInt >= 60 and hInt < 10:
        return str(round(hFloat, 1)) + "h"

    return str(hInt) + "h"


def getCurrentDirectory():
    """Get current directory (that contains python script)"""
    # TODO: Find a better way of handling paths
    return (
        os.path.dirname(os.path.realpath(__file__))
        .replace("/include", "")
        .replace("\\include", "")
    )
