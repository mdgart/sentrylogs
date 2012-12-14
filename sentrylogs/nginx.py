from conf import settings
import tailer # same functionality ad UNIX tail in python
from parsers.nginx import nginx_error_parser
from helpers import send_message

filepath = settings.NGINX_ERROR_PATH # try to read the nginx file path from settings

def nginx():

    logger = "Nginx error logs"

    for line in tailer.follow(open(filepath)):

        # create the message
        date_time_message, otherinfo = nginx_error_parser(line)
        params = [date_time_message[2],
                  date_time_message[0],
                  date_time_message[1],
                  otherinfo.get("request", "-"),
                  otherinfo.get("referrer", "-"),
                  otherinfo.get("server", "-"),
                  otherinfo.get("client", "-"),
                  otherinfo.get("host", "-"),
                  otherinfo.get("upstream", "-")]
        message ='%s' % date_time_message[2]
        extended_message =  '%s\n'\
                            'Date: %s\n'\
                            'Time: %s\n'\
                            'Request: %s\n'\
                            'Referrer: %s\n'\
                            'Server: %s\n'\
                            'Client: %s\n'\
                            'Host: %s\n'\
                            'Upstream: %s\n'
        site = otherinfo.get("referrer", "-")

        # send the message to sentry using Raven
        send_message(message, extended_message, params, site, logger)

nginx()