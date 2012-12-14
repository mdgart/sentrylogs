import os

settings = [] # to be implemented

# Sentry Nginx Error log absolute path
NGINX_ERROR_PATH = os.environ.get("NGINX_ERROR_PATH", False)
if not NGINX_ERROR_PATH:
    NGINX_ERROR_PATH = getattr(settings, "NGINX_ERROR_PATH",
        "/var/log/nginx/error.log") # absolute path to nginx error .log file

# Sentry DSN
dsn = os.environ.get("SENTRY_DSN", False)
if not dsn and settings:
    dsn = getattr(settings, "SENTRY_DSN", False)

if not dsn:
    exit("No Sentry DSN found!")

SENTRY_DSN = dsn