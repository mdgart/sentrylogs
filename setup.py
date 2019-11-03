#!/usr/bin/env python3
"""
Packaging setup for Sentry Logs
"""
from os.path import abspath, dirname, join
from setuptools import setup

import sentrylogs as package


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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
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
)
