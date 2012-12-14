===========
Sentry Logs
===========

Sentry Logs allows you to send Logs to Sentry, only Nginx error log is currently supported,
but I'm planning to extend the library to support more logs file.


How it works
============

To install sentrylogs you can use pip or easy_install::

    pip install sentrylogs

or::

    easy_install sentrylogs

This will install the module and you will have a new command line available::

    sentrylogs -h


    usage: sentrylogs [-h] [--follow FOLLOW] [--sentrydsn SENTRYDSN] [--daemonize]
                      [--nginxerrorpath NGINXERRORPATH]

    Send logs to Django Sentry.

    optional arguments:
      -h, --help            show this help message and exit
      --follow FOLLOW, -f FOLLOW
                            Which logs to follow, default ALL (for now only ALL is available)
      --sentrydsn SENTRYDSN, -s SENTRYDSN
                            The Sentry DSN string
      --daemonize, -d       Run this script in background
      --nginxerrorpath NGINXERRORPATH, -n NGINXERRORPATH
                            Nginx error log path


you must provide a Sentry DSN to make it works; at this moment you have 2 possibilities:

set up an environment variable:

$ export SENTRY_DSN="protocol://public:secret@example.com/#"
$ sentrylogs

or use the --sentrydsn argument:

$ sentrylogs --sentrydsn "protocol://public:secret@example.com/#"

By defauld it will seach for nginx log at /var/log/nginx/error.log, but you can change it using --nginxerrorpath

If you use --daemonize the command will daemonize itself and will run in background.






