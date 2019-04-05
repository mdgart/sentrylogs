"""
Helper functions for Sentry Logs
"""
from sentry_sdk import capture_message, configure_scope


def send_message(message, params, site, logger):
    """Send a message to the Sentry server"""
    msg = message % params
    with configure_scope() as scope:
        scope.set_extra('site', site)
        scope.set_extra('logger', logger)
        capture_message(msg)
