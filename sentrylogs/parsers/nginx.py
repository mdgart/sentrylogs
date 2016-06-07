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


def nginx_error_parser(line):
    """
    Parse a line of the Nginx error log.
    """
    csv_list = line.split(",")
    date_time_message = csv_list.pop(0).split(" ", 2)
    otherinfo = dict()

    for item in csv_list:
        key_value_pair = item.split(":", 1)
        key = key_value_pair[0].strip()

        # FIXME: must be > 1 or key_value_pair[1] may fail; NOTE: > 0 is always true here
        if len(key_value_pair) > 0:
            value = key_value_pair[1].strip()
            if not value:
                value = "-"
        else:
            value = "-"

        otherinfo[key] = value

    return date_time_message, otherinfo
