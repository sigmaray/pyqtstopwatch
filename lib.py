"""Helper functions that are used in stopwatch.pyw and timer.pyw"""
import sys
import datetime
import os
import json
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont, QIcon

SETTINGS_FILE = "pyqtstopwatchd.json"


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

    if not validateSettings(settings, defaultSettings):
        print(settingsFilePath + " is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings


def validateSettings(settings, defaultSettings):
    """Validate hashmap with parsed settings. Ensure that all keys are present"""
    for key in defaultSettings.keys():
        if not key in settings.keys():  # or (type(settings[key]) != int) or (settings[key] < 0):
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
    tdShort = datetime.timedelta(seconds=round(count / 10))
    tdFull = datetime.timedelta(seconds=count / 10)
    mStr = str(round(tdFull.microseconds / 100000))
    return str(tdShort) + "." + mStr


def genTextShort(count):
    """Convert int value into short time to be shown in tray"""
    seconds = count / 10
    secondsInt = round(seconds)
    minInt = round(seconds / 60)
    hFloat = float(seconds) / 60 / 60
    hInt = round(seconds / 60 / 60)

    if seconds <= 99:
        return str(secondsInt) + "s"

    if minInt < 60:
        return str(minInt) + "m"

    if minInt >= 60 and hInt < 10:
        return str(round(hFloat, 1)) + "h"

    return str(hInt) + "h"


def instanceAlreadyRunning(label="default"):
    """
    Detect if an an instance with the label is already running, globally
    at the operating system level.

    Using `os.open` ensures that the file pointer won't be closed
    by Python's garbage collector after the function's scope is exited.

    The lock will be released when the program exits, or could be
    released if the file pointer were closed.

    https://stackoverflow.com/a/384493
    """
    # In Windows fcntl is not implemented
    if sys.platform == "win32":
        return False

    import fcntl  # pylint: disable=import-outside-toplevel

    path = getCurrentDirectory() + "/" + label + '.lock'

    fle = Path(path)
    fle.touch(exist_ok=True)

    lockFilePointer = os.open(path, os.O_WRONLY)

    try:
        fcntl.lockf(lockFilePointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        alreadyRunning = False
    except IOError:
        alreadyRunning = True

    return alreadyRunning


def getCurrentDirectory():
    """Get current directory (that contains python script)"""
    return os.path.dirname(os.path.realpath(__file__))
