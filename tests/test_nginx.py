"""
Tests for the command line interface (CLI)
"""
from sentrylogs.parsers.nginx import Nginx


def test_regex():
    """
    Test that the regex works for nginx logs
    """
    logs = (
        "2019/04/05 12:01:47 [error] 1895#1895: *5 connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
        "2019/04/05 12:01:47 [error] 1895#1895: *5connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
    )
    date = "2019/04/05"
    time = "12:01:47"
    level = "error"
    pid = "1895"
    tid = "1895"
    message = "connect() failed (111: Connection refused) while connecting to upstream"  # noqa: E501

    n = Nginx()
    for log in logs:
        n.clear_attributes()
        n.parse(log)
        assert date == n.data["date"]
        assert time == n.data["time"]
        assert level == n.level
        assert pid == n.data['pid']
        assert tid == n.data["tid"]
        assert "5" == n.data["cid"]
        assert message == n.message

    # According to https://stackoverflow.com/a/26125951 the *cid is optional
    cid_optional = (
        "2019/04/05 12:01:47 [error] 1895#1895: *connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
        "2019/04/05 12:01:47 [error] 1895#1895: connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
        "2019/04/05 12:01:47 [error] 1895#1895: 5connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
    )
    for log in cid_optional:
        n.clear_attributes()
        n.parse(log)
        assert date == n.data["date"]
        assert time == n.data["time"]
        assert level == n.level
        assert pid == n.data['pid']
        assert tid == n.data["tid"]
        assert None is n.data["cid"]

    messages = (
        "*connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
        "connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
        "5connect() failed (111: Connection refused) while connecting to upstream",  # noqa: E501
    )
    for log, message in zip(cid_optional, messages):
        n.clear_attributes()
        n.parse(log)
        assert message == n.message


def test_error_does_not_match_regex():
    """
    Test when the regex does not match
    """
    logs = (
        'nginx: [emerg] open() "/etc/nginx/mime.types" failed (2: No such file or directory) in /opt/bitnami/nginx/conf/server_blocks/server-block.conf:24',  # noqa: E501
    )

    level = "fatal"

    n = Nginx()
    for log in logs:
        message = log
        n.clear_attributes()
        n.parse(log)
        assert level == n.level
        assert message == n.message
