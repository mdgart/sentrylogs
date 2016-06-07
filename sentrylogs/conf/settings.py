"""
Default settings for Sentry Logs, and handling of their values.
"""
import os

settings = []  # to be implemented  # pylint: disable=invalid-name

# Sentry Nginx Error log absolute path
NGINX_ERROR_PATH = os.environ.get("NGINX_ERROR_PATH", False)
if not NGINX_ERROR_PATH:
    # absolute path to nginx error .log file
    NGINX_ERROR_PATH = getattr(
        settings, "NGINX_ERROR_PATH", "/var/log/nginx/error.log")

# Sentry DSN
SENTRY_DSN = os.environ.get("SENTRY_DSN", False)
if not SENTRY_DSN and settings:
    SENTRY_DSN = getattr(settings, "SENTRY_DSN", False)

if not SENTRY_DSN:
    exit("No Sentry DSN found!")
