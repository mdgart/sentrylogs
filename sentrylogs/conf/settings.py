"""
Default settings for Sentry Logs, and handling of their values.
"""
import os

import sentry_sdk


# absolute path to nginx error .log file
NGINX_ERROR_PATH = os.environ.get('NGINX_ERROR_PATH',
                                  '/var/log/nginx/error.log')

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
sentry_sdk.init(SENTRY_DSN)
