"""
Tests for the command line interface (CLI)
"""
import os
import pytest
from unittest.mock import patch

from sentrylogs.bin.sentrylogs import main

from helpers import ArgvContext, EnvironContext


def test_entrypoint():
    """
    Was the entrypoint script installed? (setup.py)
    """
    exit_status = os.system('sentrylogs --help')
    assert exit_status == 0


def test_fail_without_sentrydns():
    """
    Must fail without a ``SENTRY_DSN`` environment variable specified
    """
    explain_failure = "Should have failed w/o SENTRY_DSN environment variable"

    with EnvironContext(SENTRY_DSN=None), ArgvContext('--daemonize'):
        with pytest.raises(SystemExit, message=explain_failure):
            main()


@patch('sentrylogs.bin.sentrylogs.launch_log_parsers')
def test_pass_with_sentrydns(mock_launch_log_parsers):
    """
    Must pass with a ``SENTRY_DSN`` environment variable available
    """
    sentry_dns = 'https://username:password@sentry.example.com/project'

    with EnvironContext(SENTRY_DSN=sentry_dns), ArgvContext('--daemonize'):
        main()

    assert mock_launch_log_parsers.called, "Log parsing didn't start"
