"""
Default settings for Sentry Logs, and handling of their values.
"""
import os

# absolute path to nginx error .log file
NGINX_ERROR_PATH = os.environ.get('NGINX_ERROR_PATH',
                                  '/var/log/nginx/error.log')

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
if not SENTRY_DSN:
    raise SystemExit('No Sentry DSN found!')
