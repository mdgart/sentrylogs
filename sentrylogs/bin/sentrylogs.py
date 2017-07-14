#!/usr/bin/env python
"""Standalone script for Sentry Logs"""
from __future__ import print_function

import argparse
import os

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
                        help='A configuration file (.ini, .yaml) of some Sentry integration'
                             ' to extract the Sentry DSN from')
    parser.add_argument('--sentrydsn', '-s', default="",
                        help='The Sentry DSN string (overrides -c)')
    parser.add_argument('--daemonize', '-d', action='store_const', const=True, default=False,
                        help='Run this script in background')
    parser.add_argument('--follow', '-f', default="all", help='Which logs to follow, default ALL')
    parser.add_argument('--nginxerrorpath', '-n', default=None, help='Nginx error log path')

    return parser.parse_args()


def process_arguments(args):
    """Deal with arguments passed on the command line"""
    if args.sentryconfig:
        print('Parsing DSN from %s' % args.sentryconfig)
        os.environ['SENTRY_DSN'] = parse_sentry_configuration(args.sentryconfig)

    if args.sentrydsn:
        print('Using the DSN %s' % args.sentrydsn)
        os.environ['SENTRY_DSN'] = args.sentrydsn

    if args.nginxerrorpath:
        print('Using the Nginx error log path %s' % args.nginxerrorpath)
        os.environ['NGINX_ERROR_PATH'] = args.nginxerrorpath

    from ..conf import settings  # noqa; pylint: disable=unused-variable

    if args.daemonize:
        print('Running process in background')
        from ..daemonize import create_daemon
        create_daemon()


def parse_sentry_configuration(filename):
    """Parse Sentry DSN out of an application or Sentry configuration file"""
    filetype = os.path.splitext(filename)[-1][1:].lower()

    if filetype == 'ini':  # Pyramid, Pylons
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
                    print('- Warning: Key "{key}" not found in section [{section}]'
                          .format(section=section, key=ini_key))
        exit('No DSN found in {file}. Tried sections [{sec_list}]'
             .format(file=filename, sec_list='], ['.join(ini_sections)))
    elif filetype == 'py':  # Django, Flask, Bottle, ...
        exit('Parsing configuration from pure Python (Django, Flask, Bottle, etc.)'
             ' not implemented yet.')
    else:
        exit('Configuration file type not supported for parsing: %s' % filetype)


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
