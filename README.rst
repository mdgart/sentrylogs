============================
Sentry Logs |latest-version|
============================

|build-status| |health| |python-support| |license|

Sentry Logs allows you to send logs to Sentry.  Only Nginx error log is
currently supported, but extending the library to support more log files
is planned.


.. |latest-version| image:: https://img.shields.io/pypi/v/sentrylogs.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/sentrylogs
.. |build-status| image:: https://travis-ci.org/mdgart/sentrylogs.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/mdgart/sentrylogs
.. |health| image:: https://landscape.io/github/mdgart/sentrylogs/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mdgart/sentrylogs/master
   :alt: Code health
.. |python-support| image:: https://img.shields.io/pypi/pyversions/sentrylogs.svg
   :target: https://pypi.python.org/pypi/sentrylogs
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/sentrylogs.svg
   :alt: Software license
   :target: https://github.com/mdgart/sentrylogs/blob/master/LICENSE.txt

How It Works
============

To install *sentrylogs* you can use pip or easy_install:

.. code-block:: bash

    $ pip install sentrylogs

.. code-block:: bash

    $ easy_install sentrylogs

This will install the module and will provide a new console command:

.. code-block:: bash

    $ sentrylogs -h

    usage: sentrylogs [-h] [--sentryconfig SENTRYCONFIG] [--sentrydsn SENTRYDSN]
                      [--daemonize] [--follow FOLLOW]
                      [--nginxerrorpath NGINXERRORPATH]

    Send logs to Django Sentry.

    optional arguments:
      -h, --help            show this help message and exit
      --sentryconfig SENTRYCONFIG, -c SENTRYCONFIG
                            A configuration file (.ini, .yaml) of some Sentry
                            integration to extract the Sentry DSN from
      --sentrydsn SENTRYDSN, -s SENTRYDSN
                            The Sentry DSN string (overrides -c)
      --daemonize, -d       Run this script in background
      --follow FOLLOW, -f FOLLOW
                            Which logs to follow, default ALL
      --nginxerrorpath NGINXERRORPATH, -n NGINXERRORPATH
                            Nginx error log path

Sentry DSN
----------

We need to provide a Sentry DSN to send messages to the Sentry server.  There
are 3 options to do this:

#. Use the ``--sentryconfig`` command line argument to read the configuration
   file of your `Sentry integration`_, or
#. Use the ``--sentrydsn`` command line argument to specify the DSN directly, or
#. Provide an environment variable.

.. code-block:: bash

    $ sentrylogs --sentryconfig /opt/myapp/config/pyramid.ini
    $ sentrylogs --sentrydsn 'protocol://public:secret@example.com/#'
    $ export SENTRY_DSN='protocol://public:secret@example.com/#' && sentrylogs

Log File Location
-----------------

By default *sentrylogs* will assume the nginx log at ``/var/log/nginx/error.log``.
You can change this using the ``--nginxerrorpath`` argument.

Run as Daemon
-------------

If you use ``--daemonize`` the command will daemonize itself and run in
background.


.. _Sentry integration: https://docs.getsentry.com/on-premise/clients/python/#deep-dive

How to Contribute
=================

Please `open an issue`_ to discuss your plans for a `pull request`_.  After
writing code make sure your changes pass our quality gate before you push.

.. code-block:: console

    # list all tox targets
    tox -lv

    # run all linting and tests
    tox

    # run tests just for Python 3.8
    # (e.g. if you don't have all Pythons installed via pyenv)
    tox -e py38

Please write tests!  Test coverage is still low and the code quality needs
to improve.  Please help by adding tests with each contribution you make!


.. _open an issue: https://github.com/mdgart/sentrylogs/issues
.. _pull request: https://github.com/mdgart/sentrylogs/pulls
