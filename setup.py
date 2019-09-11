#!/usr/bin/env python3
"""Packaging implementation for Sentry Logs"""
from __future__ import print_function

from glob import glob
import os
from os.path import abspath, dirname, join
import shutil

from setuptools import Command, setup

import sentrylogs as package


class SimpleCommand(Command):
    """A simple setuptools command (implementation of abstract base class)"""
    user_options = []

    def initialize_options(self):
        """Abstract method of the base class (required to be overridden)"""

    def finalize_options(self):
        """Abstract method of the base class (required to be overridden)"""


class Clean(SimpleCommand):
    """Remove build files and folders, including Python byte-code"""
    description = __doc__

    @staticmethod
    def run():
        """
        Clean up files not meant for version control
        """
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
    """Platform independent rmtree, which also allows wildcards (globbing)"""
    for item in glob(file_glob, recursive=True):
        try:
            os.remove(item)
            print('%s removed ...' % item)
        except OSError:
            try:
                shutil.rmtree(item)
                print('%s/ removed ...' % item)
            except OSError as err:
                print(err)


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as file:
        return file.read()


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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    license=package.__license__,
    url=package.__url__,
    install_requires=read_file('requirements.txt'),
    entry_points={
        'console_scripts': [
            'sentrylogs = sentrylogs.bin.sentrylogs:main',
        ],
    },
    packages=[
        'sentrylogs',
        'sentrylogs.bin',
        'sentrylogs.conf',
        'sentrylogs.parsers',
    ],
    test_suite='tests',
    tests_require=['tox'],
    cmdclass={
        'clean': Clean,
    },
)
