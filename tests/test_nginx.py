"""
Tests for the command line interface (CLI)
"""
import os
import pytest

from sentrylogs.parsers.nginx import Nginx

def test_regex():
    """
    Test that the regex works for nginx logs
    """
    logs = (
        "2019/04/05 12:01:47 [error] 1895#1895: *5 connect() failed (111: Connection refused) while connecting to upstream",
        "2019/04/05 12:01:47 [error] 1895#1895: *5connect() failed (111: Connection refused) while connecting to upstream",
    )
    date = "2019/04/05"
    time = "12:01:47"
    level = "error"
    pid = "1895"
    tid = "1895"
    message = "connect() failed (111: Connection refused) while connecting to upstream"

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
        "2019/04/05 12:01:47 [error] 1895#1895: *connect() failed (111: Connection refused) while connecting to upstream",
        "2019/04/05 12:01:47 [error] 1895#1895: connect() failed (111: Connection refused) while connecting to upstream",
        "2019/04/05 12:01:47 [error] 1895#1895: 5connect() failed (111: Connection refused) while connecting to upstream",
    )
    for log in cid_optional:
        n.clear_attributes()
        n.parse(log)
        assert date == n.data["date"]
        assert time == n.data["time"]
        assert level == n.level
        assert pid == n.data['pid']
        assert tid == n.data["tid"]
        assert None == n.data["cid"]
    
    messages = (
        "*connect() failed (111: Connection refused) while connecting to upstream",
        "connect() failed (111: Connection refused) while connecting to upstream",
        "5connect() failed (111: Connection refused) while connecting to upstream",
    )
    for log, message in zip(cid_optional, messages):
        n.clear_attributes()
        n.parse(log)
        assert message == n.message
