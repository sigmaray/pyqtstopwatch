""" Limits application to single instance (in Windows) """
import sys
if sys.platform == "win32":
    from win32event import CreateMutex  # pylint: disable=import-error
    from win32api import CloseHandle, GetLastError  # pylint: disable=import-error


class SingleInstanceWindows:
    """ Limits application to single instance (in Windows) """

    def __init__(self):
        super().__init__()

        if sys.platform == "win32":
            label = self.__class__.__name__
            uuid = "8fd7eea4-f219-11ed-a05b-0242ac120003"
            mutexName = label + "{" + uuid + "}"
            self.mutex = CreateMutex(None, False, mutexName)
            self.lasterror = GetLastError()

    def isAlreadyRunningWindows(self):
        """Check if another instance of app is already opened"""
        return sys.platform == "win32" and self.lasterror != 0

    def __del__(self):
        if hasattr(super(), '__del__') and callable(super().__del__):  # pylint: disable=no-member
            super().__del__()  # pylint: disable=no-member

        if sys.platform == "win32" and self.mutex:
            CloseHandle(self.mutex)
