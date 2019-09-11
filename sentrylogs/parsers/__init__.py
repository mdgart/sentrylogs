"""
Log file parsers provided by Sentry Logs
"""
import time

import tailhead  # same functionality as UNIX tail in python

from ..helpers import send_message

try:
    (FileNotFoundError, PermissionError)
except NameError:  # Python 2.7
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin
    PermissionError = IOError  # pylint: disable=redefined-builtin


class Parser(object):  # pylint: disable=useless-object-inheritance
    """Abstract base class for any parser"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.logger = self.__doc__.strip()
        self.message = None
        self.level = None
        self.data = {
            "logger": self.logger,
        }

    def clear_attributes(self):
        """Reset attributes"""
        self.message = None
        self.level = None
        self.data = {
            "logger": self.logger,
        }

    def follow_tail(self):
        """
        Read (tail and follow) the log file, parse entries and send messages
        to Sentry using Raven.
        """

        try:
            follower = tailhead.follow_path(self.filepath)
        except (FileNotFoundError, PermissionError) as err:
            raise SystemExit("Error: Can't read logfile %s (%s)" %
                             (self.filepath, err))

        for line in follower:
            self.clear_attributes()

            if line is not None:
                self.parse(line)
                send_message(
                    self.message,
                    self.level,
                    self.data,
                )
            else:
                time.sleep(1)

    def parse(self, line):
        """
        Parse a line of a log file.  Must be overridden by the subclass.
        The implementation must set these properties:

        - ``message`` (string)
        - ``level`` (string)

        Additional optional properties:
        - ``data`` (dict)
        """
        raise NotImplementedError('parse() method must set: '
                                  'message, level')
