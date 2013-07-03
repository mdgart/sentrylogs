#
# parse a tipical nginx error log like this
#
# 2012/11/29 19:30:02
# [error] 15596#0: *4 open() "/srv/active/collected-static/50x.html" failed (2: No such file or directory),
# client: 65.44.217.34,
# server: ,
# request: "GET /api/megapage/poll/?cursor=1354216956 HTTP/1.1",
# upstream: "http://0.0.0.0:9000/api/megapage/poll/?cursor=1354216956",
# host: "165.225.132.103",
# referrer: "http://165.225.132.103/megapage/"


from string import strip

def nginx_error_parser(line):
    csv_list = line.split(",")
    date_time_message = csv_list.pop(0).split(" ",2)
    otherinfo = dict()

    for l in csv_list:
        kv = l.split(":",1)
        if len(kv)>0:
            value = strip(kv[1])
            if not value:
                value = "-"
        else:
            value = "-"
        otherinfo[strip(kv[0])] = value

    return date_time_message, otherinfo
