"""
Helper functions for Sentry Logs
"""
from sentry_sdk import capture_message, configure_scope

from .conf.settings import SENTRY_LOG_LEVEL, SENTRY_LOG_LEVELS


def send_message(message, level, data):
    """Send a message to the Sentry server"""
    # Only send messages for desired log level
    if (SENTRY_LOG_LEVELS.index(level)
            < SENTRY_LOG_LEVELS.index(SENTRY_LOG_LEVEL)):
        return
    with configure_scope() as scope:
        for key, value in data.items():
            scope.set_extra(key, value)
        capture_message(message, level)
