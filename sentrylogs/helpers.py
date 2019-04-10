"""
Helper functions for Sentry Logs
"""
from sentry_sdk import capture_message, configure_scope


def send_message(message, level, data):
    """Send a message to the Sentry server"""
    with configure_scope() as scope:
        for key, value in data.items():
            scope.set_extra(key, value)
        capture_message(message, level)
