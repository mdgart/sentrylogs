"""
Tests for our tests helpers  8-}
"""
import os
import sys

from helpers import ArgvContext, EnvironContext


def test_argv_context():
    """
    Test if ArgvContext sets the right argvs and resets to the old correctly
    """
    old = sys.argv
    new = ["Alice", "Bob", "Chris", "Daisy"]

    assert sys.argv == old

    with ArgvContext(*new):
        assert sys.argv == new, \
            "sys.argv wasn't correctly changed by the contextmanager"

    assert sys.argv == old, "sys.argv wasn't correctly reset"


def test_environ_context():
    """
    Test if EnvironContext sets the right environ values and resets to
    the old values correctly
    """
    old = os.environ
    new = {'PATH': None, 'FOO': 'my foo value'}

    assert os.environ == old
    assert os.environ.get('PATH'), "Invalid test setup"
    assert not os.environ.get('FOO'), "Invalid test setup"

    with EnvironContext(**new):
        assert not os.environ.get('PATH'), \
            "os.environ[PATH] wasn't removed by the contextmanager"
        assert os.environ['FOO'] == new['FOO'], \
            "os.environ[FOO] wasn't set by the contextmanager"

    assert os.environ == old, "os.environ wasn't correctly reset"
