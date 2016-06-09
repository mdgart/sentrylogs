"""
Log file parsers provided by Sentry Logs
"""
import tailer  # same functionality as UNIX tail in python

from ..helpers import send_message


class Parser(object):
    """Abstract base class for any parser"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.logger = self.__doc__.strip()
        self.message = None
        self.extended_message = None
        self.params = None
        self.site = None

    def follow_tail(self):
        """
        Read (tail and follow) the log file, parse entries and send messages
        to Sentry using Raven.
        """
        for line in tailer.follow(open(self.filepath)):
            self.message = None
            self.extended_message = None
            self.params = None
            self.site = None

            self.parse(line)
            send_message(self.message,
                         self.extended_message,
                         self.params,
                         self.site,
                         self.logger)

    def parse(self, line):
        """
        Parse a line of a log file.  Must be overridden by the subclass.
        The implementation must set these properties:

        - ``message`` (string)
        - ``extended_message`` (string)
        - ``params`` (list of string)
        - ``site`` (string)
        """
        raise NotImplementedError('parse() method must set: '
                                  'message, extended_message, params, site')
