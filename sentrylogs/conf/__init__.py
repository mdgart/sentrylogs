"""
Configuration of Sentry Logs
"""
from raven import Client

from .settings import SENTRY_DSN

client = Client(dsn=SENTRY_DSN)  # pylint: disable=invalid-name
