""" Limits application to single instance (in Unix) """
import sys
import os
from pathlib import Path
if sys.platform != "win32":
    import fcntl
import helpers  # pylint: disable=wrong-import-position


class SingleInstanceUnix:
    """ Limits application to single instance (in Unix) """

    def __init__(self):
        """
        Detect if an an instance with the label is already running, globally
        at the operating system level.

        Using `os.open` ensures that the file pointer won't be closed
        by Python's garbage collector after the function's scope is exited.

        The lock will be released when the program exits, or could be
        released if the file pointer were closed.

        https://stackoverflow.com/a/384493
        """

        super().__init__()

        if sys.platform == "win32":
            return

        label = self.__class__.__name__

        self.path = helpers.getCurrentDirectory() + "/" + label + '.lock'

        fle = Path(self.path)
        fle.touch(exist_ok=True)

        self.lock_file_fd = os.open(self.path, os.O_WRONLY)

        try:
            fcntl.lockf(self.lock_file_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.alreadyRunningUnix = False
        except IOError:
            self.alreadyRunningUnix = True

    def isAlreadyRunningUnix(self):
        """Check if another instance of app is already opened"""
        return sys.platform != "win32" and self.alreadyRunningUnix

    def __del__(self):
        if hasattr(super(), "__del__") and callable(super().__del__):  # pylint: disable=no-member
            super().__del__()  # pylint: disable=no-member

        if sys.platform == "win32":
            return

        fcntl.flock(self.lock_file_fd, fcntl.LOCK_UN)
        os.close(self.lock_file_fd)
        Path(self.path).unlink()
