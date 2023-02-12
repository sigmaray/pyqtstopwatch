from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime
import os
import json
import fcntl

from pathlib import Path

SETTINGS_FILE = "pyqtstopwatchd.json"

def doSettingsExist(settings_file_path):
    return os.path.isfile(get_current_directory() + "/" + settings_file_path)

def writeSettingsFile(settings_file_path, hashmap):
    with open(get_current_directory() + "/" + settings_file_path, 'w') as f:
        f.write(json.dumps(hashmap))

def readSettingsFile(settings_file_path):
    with open(get_current_directory() + "/" + settings_file_path) as f:
        return json.load(f)

def readWriteSettings(settings_file_path, default_settings):
    if not doSettingsExist(settings_file_path):
        print(settings_file_path + " does not exist, creating it")
        writeSettingsFile(settings_file_path, default_settings)

    settings = readSettingsFile(settings_file_path)

    if not validateSettings(settings, default_settings):
        print(settings_file_path + " is not valid. " +
              "You can delete it and restart the application. " +
              "App will recreate settings file if it's not present")
        sys.exit()

    return settings

def validateSettings(settings, default_settings):
    # for key in ["checkIsOut", "checkIsColliding"]:
    #     if not(key in settings.keys()) or (type(settings[key]) != bool):
    #         return False

    # for key in ["cellNum", "intervalMilliseconds"]:
    #     if not(key in settings.keys()) or (type(settings[key]) != int) or (settings[key] < 0):
    #         return False

    # if settings["cellNum"] < 2:
    #     return False

    for key in default_settings.keys():
        # key = "count"
        if not(key in settings.keys()): # or (type(settings[key]) != int) or (settings[key] < 0):
            return False

    return True

def drawIcon(strVal="--", textColor = "#000", bgColor = "#fff"):
    pixmap = QPixmap(24, 24)
    pixmap.fill(QColor(bgColor))

    painter = QPainter(pixmap)
    painter.setPen(QColor(textColor))

    if len(strVal) >= 3:
        fontSize = 10
    else:
        fontSize = 12
    # print("fontSize " + str(fontSize) + ", strVal: " + strVal)
    painter.setFont(QFont('Arial', fontSize))

    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, strVal)
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

def instance_already_running(label="default"):
    """
    Detect if an an instance with the label is already running, globally
    at the operating system level.

    Using `os.open` ensures that the file pointer won't be closed
    by Python's garbage collector after the function's scope is exited.

    The lock will be released when the program exits, or could be
    released if the file pointer were closed.
    """
    
    path = get_current_directory() + "/" + label + '.lock'

    fle = Path(path)
    fle.touch(exist_ok=True)

    # lock_file_pointer = os.open(f"/tmp/instance_{label}.lock", os.O_WRONLY)
    lock_file_pointer = os.open(path, os.O_WRONLY)

    try:
        fcntl.lockf(lock_file_pointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        already_running = False
    except IOError:
        already_running = True

    return already_running

def get_current_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print("SCript path:", dir_path)
    return dir_path


