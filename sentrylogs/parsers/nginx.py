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
from . import Parser
from ..conf.settings import NGINX_ERROR_PATH


class Nginx(Parser):
    """Nginx error logs"""

    def __init__(self):
        super(Nginx, self).__init__(NGINX_ERROR_PATH)

    def parse(self, line):
        """Parse a line of the Nginx error log"""
        csv_list = line.split(",")
        date_time_message = csv_list.pop(0).split(" ", 2)
        otherinfo = dict()

        for item in csv_list:
            key_value_pair = item.split(":", 1)
            key = key_value_pair[0].strip()

            if len(key_value_pair) > 1:
                value = key_value_pair[1].strip()
                if not value:
                    value = "-"
            else:
                value = "-"

            otherinfo[key] = value

        self.message = '%s\n' \
                       'Date: %s\n' \
                       'Time: %s\n' \
                       'Request: %s\n' \
                       'Referrer: %s\n' \
                       'Server: %s\n' \
                       'Client: %s\n' \
                       'Host: %s\n' \
                       'Upstream: %s\n'
        self.params = [
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
        self.site = otherinfo.get("referrer", "-")
