"""
Useful helpers for our tests
"""
import os
import sys


class ArgvContext:
    """
    A simple context manager allowing to temporarily override ``sys.argv``
    """

    def __init__(self, *new_args):
        self._old = sys.argv
        self.args = type(self._old)(new_args)

    def __enter__(self):
        sys.argv = self.args

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.argv = self._old


class EnvironContext:
    """
    A simple context manager allowing to temporarily set environment values
    """

    def __init__(self, **kwargs):
        self._old = os.environ
        self._kwargs = kwargs

    def __enter__(self):
        for key in self._kwargs:
            if self._kwargs[key] is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = self._kwargs[key]

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.environ = self._old
