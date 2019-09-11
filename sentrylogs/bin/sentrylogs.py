#!/usr/bin/env python
"""Standalone script for Sentry Logs"""
from __future__ import print_function

import os
import argparse

try:
    from configparser import ConfigParser
except ImportError:  # Python 2.7
    from ConfigParser import ConfigParser  # pylint: disable=import-error


# Ignore warnings caused by ``sentrylogs.<...>`` imports
# pylint: disable=no-name-in-module

def get_command_line_args():
    """CLI command line arguments handling"""
    parser = argparse.ArgumentParser(description='Send logs to Django Sentry.')

    parser.add_argument('--sentryconfig', '-c', default=None,
                        help='A configuration file (.ini, .yaml) of some '
                             'Sentry integration to extract the Sentry DSN from')
    parser.add_argument('--sentrydsn', '-s', default="",
                        help='The Sentry DSN string (overrides -c)')
    parser.add_argument('--daemonize', '-d', default=False,
                        action='store_const', const=True,
                        help='Run this script in background')
    parser.add_argument('--follow', '-f', default="all",
                        help='Which logs to follow, default ALL')
    parser.add_argument('--nginxerrorpath', '-n', default=None,
                        help='Nginx error log path')
    parser.add_argument('--loglevel', '-l', default=None,
                        help='Minimum log level to send to sentry')

    return parser.parse_args()


def process_arguments(args):
    """Deal with arguments passed on the command line"""
    if args.sentryconfig:
        print('Parsing DSN from %s' % args.sentryconfig)
        os.environ['SENTRY_DSN'] = parse_sentry_configuration(args.sentryconfig)

    if args.sentrydsn:
        print('Using the DSN %s' % args.sentrydsn)
        os.environ['SENTRY_DSN'] = args.sentrydsn
    if ('SENTRY_DSN' not in os.environ) or (not os.environ['SENTRY_DSN']):
        raise SystemExit('No Sentry DSN found!')

    if args.nginxerrorpath:
        print('Using the Nginx error log path %s' % args.nginxerrorpath)
        os.environ['NGINX_ERROR_PATH'] = args.nginxerrorpath

    if args.loglevel:
        print('Using the sentry log level %s' % args.loglevel)
        os.environ['SENTRY_LOG_LEVEL'] = args.loglevel

    from ..conf import settings  # noqa: F401; pylint: disable=unused-import

    if args.daemonize:
        print('Running process in background')
        from ..daemonize import create_daemon
        create_daemon()


def parse_sentry_configuration(filename):
    """Parse Sentry DSN out of an application or Sentry configuration file"""
    filetype = os.path.splitext(filename)[-1][1:].lower()

    if filetype == 'ini':  # Pyramid, Pylons # pylint: disable=no-else-raise
        config = ConfigParser()
        config.read(filename)
        ini_key = 'dsn'
        ini_sections = ['sentry', 'filter:raven']

        for section in ini_sections:
            if section in config:
                print('- Using value from [{section}]:[{key}]'
                      .format(section=section, key=ini_key))
                try:
                    return config[section][ini_key]
                except KeyError:
                    print('- Warning: Key "{key}" not found in section '
                          '[{section}]'.format(section=section, key=ini_key))
        raise SystemExit('No DSN found in {file}. Tried sections [{sec_list}]'
                         .format(
                             file=filename,
                             sec_list='], ['.join(ini_sections),
                         ))
    elif filetype == 'py':  # Django, Flask, Bottle, ...
        raise SystemExit('Parsing configuration from pure Python (Django,'
                         'Flask, Bottle, etc.) not implemented yet.')
    raise SystemExit('Configuration file type not supported for parsing: '
                     '%s' % filetype)


def launch_log_parsers():
    """Run all log file parsers that send entries to Sentry"""
    from ..parsers.nginx import Nginx

    for parser in [Nginx]:
        parser().follow_tail()


def main():
    """Main entry point of console script"""
    args = get_command_line_args()
    process_arguments(args)
    print('Start sending %s logs to Sentry' % args.follow)
    launch_log_parsers()


if __name__ == '__main__':
    main()
