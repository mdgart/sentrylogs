"""
Default settings for Sentry Logs, and handling of their values.
"""
import os

import sentry_sdk

SENTRY_LOG_LEVELS = (
    "debug",
    "info",
    "warning",
    "error",
    "fatal",
)

# absolute path to nginx error .log file
NGINX_ERROR_PATH = os.environ.get('NGINX_ERROR_PATH',
                                  '/var/log/nginx/error.log')

SENTRY_LOG_LEVEL = os.environ.get('SENTRY_LOG_LEVEL', 'error')
if SENTRY_LOG_LEVEL not in SENTRY_LOG_LEVELS:
    MESSAGE = "Log level '{}' is invalid. Valid options are {}".format(
        SENTRY_LOG_LEVEL,
        SENTRY_LOG_LEVELS,
    )
    raise SystemExit(MESSAGE)

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
sentry_sdk.init(SENTRY_DSN)
