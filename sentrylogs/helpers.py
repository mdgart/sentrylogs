"""
Helper functions for Sentry Logs
"""
from .conf import client


def send_message(message, params, site, logger):
    """Send a message to the Sentry server"""
    client.capture(
        'Message',
        message=message,
        params=tuple(params),
        data={
            'site': site,
            'logger': logger,
        },
    )
