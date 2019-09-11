"""
Parse a typical nginx error log, such as:

2012/11/29 19:30:02
[error] 15596#0: *4 open() "/srv/active/collected-static/50x.html" failed
 (2: No such file or directory),
client: 65.44.217.34,
server: ,
request: "GET /api/megapage/poll/?cursor=1354216956 HTTP/1.1",
upstream: "http://0.0.0.0:9000/api/megapage/poll/?cursor=1354216956",
host: "165.225.132.103",
referrer: "http://165.225.132.103/megapage/"
"""
from __future__ import print_function

import re
import sys

from . import Parser
from ..conf.settings import NGINX_ERROR_PATH


class Nginx(Parser):
    """Nginx error logs"""

    def __init__(self):
        super(Nginx, self).__init__(NGINX_ERROR_PATH)
        self.pattern = r"^(?P<date>\S+) (?P<time>\S+) \[(?P<level>[^\]]+)\] (?P<pid>\d+)\#(?P<tid>\d+)\:(?: \*(?P<cid>\d+))? ?(?P<message>.+)"  # noqa: E501; pylint: disable=line-too-long
        self.nginx_to_sentry = {
            "debug": "debug",
            "info": "info",
            "notice": "info",
            "warn": "warning",
            "error": "error",
            "crit": "fatal",
            "alert": "fatal",
            "emerg": "fatal",
        }

    def get_sentry_log_level(self, level):
        """ Get the Sentry log level given the nginx log level"""
        return self.nginx_to_sentry[level]

    def parse(self, line):
        """Parse a line of the Nginx error log"""
        print(line, file=sys.stderr)
        sys.stderr.flush()

        csv_list = line.split(",")

        regex = re.match(self.pattern, csv_list.pop(0))
        self.data["date"] = regex.group("date")
        self.data["time"] = regex.group("time")
        self.level = self.get_sentry_log_level(regex.group("level"))
        self.data["pid"] = regex.group("pid")
        self.data["tid"] = regex.group("tid")
        self.data["cid"] = regex.group("cid")
        self.message = regex.group("message")

        for item in csv_list:
            key_value_pair = item.split(":", 1)
            key = key_value_pair[0].strip()

            if len(key_value_pair) > 1:
                value = key_value_pair[1].strip()
                if not value:
                    value = "-"
            else:
                value = "-"

            self.data[key] = value
