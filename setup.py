#!/usr/bin/env python
"""Setup for Sentry Logs"""
from __future__ import print_function

from glob import glob
from os import remove
from os.path import abspath, dirname, join
from shlex import split
from shutil import rmtree

from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa N812

import sentrylogs as package


class Tox(TestCommand):
    """Integration of tox via the setuptools ``test`` command"""
    # pylint: disable=attribute-defined-outside-init
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline  # pylint: disable=import-error
        args = self.tox_args
        if args:
            args = split(self.tox_args)
        cmdline(args=args)


class Clean(TestCommand):
    """A setuptools ``clean`` command. Removes build files and folders"""

    def run(self):
        delete_in_root = [
            'build',
            'dist',
            '.eggs',
            '*.egg-info',
            '.tox',
        ]
        delete_everywhere = [
            '*.pyc',
            '__pycache__',
        ]
        for candidate in delete_in_root:
            rmtree_glob(candidate)
        for visible_dir in glob('[A-Za-z0-9_]*'):
            for candidate in delete_everywhere:
                rmtree_glob(join(visible_dir, candidate))
                rmtree_glob(join(visible_dir, '*', candidate))
                rmtree_glob(join(visible_dir, '*', '*', candidate))


def rmtree_glob(file_glob):
    """Platform independent rmtree. Removes a complete directory."""
    for fobj in glob(file_glob):
        try:
            rmtree(fobj)
            print('%s/ removed ...' % fobj)
        except OSError:
            try:
                remove(fobj)
                print('%s removed ...' % fobj)
            except OSError as err:
                print(err)


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


setup(
    name='SentryLogs',
    version=package.__version__,
    author=package.__author__,
    author_email=package.__author_email__,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    license=package.__license__,
    url=package.__url__,
    install_requires=read_file('requirements.txt'),
    scripts=['bin/sentrylogs'],
    packages=['sentrylogs', 'sentrylogs.conf', 'sentrylogs.parsers'],
    test_suite='tests',
    tests_require=['tox'],
    cmdclass={
        'clean': Clean,
        'test': Tox,
    },
)
