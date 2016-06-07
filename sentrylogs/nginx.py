"""
Log reader for Nginx error log.
"""
import tailer  # same functionality as UNIX tail in python

from .conf.settings import NGINX_ERROR_PATH
from .helpers import send_message
from .parsers.nginx import nginx_error_parser


def nginx():
    """
    Read (tail and follow) Nginx error log, parse entries and send messages
    to Sentry using Raven.
    """
    logger = "Nginx error logs"

    for line in tailer.follow(open(NGINX_ERROR_PATH)):
        date_time_message, otherinfo = nginx_error_parser(line)
        params = [
            date_time_message[2],
            date_time_message[0],
            date_time_message[1],
            otherinfo.get("request", "-"),
            otherinfo.get("referrer", "-"),
            otherinfo.get("server", "-"),
            otherinfo.get("client", "-"),
            otherinfo.get("host", "-"),
            otherinfo.get("upstream", "-"),
        ]
        message = '%s' % date_time_message[2]
        extended_message = '%s\n' \
                           'Date: %s\n' \
                           'Time: %s\n' \
                           'Request: %s\n' \
                           'Referrer: %s\n' \
                           'Server: %s\n' \
                           'Client: %s\n' \
                           'Host: %s\n' \
                           'Upstream: %s\n'
        site = otherinfo.get("referrer", "-")
        send_message(message, extended_message, params, site, logger)


nginx()
