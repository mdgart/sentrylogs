from setuptools import setup

setup(
    name='SentryLogs',
    version='0.0.7',
    author='Mauro De Giorgi',
    author_email='mauro.degiorgi@gmail.com',
    scripts=['bin/sentrylogs',],
    packages=['sentrylogs', 'sentrylogs.conf', 'sentrylogs.parsers'],
    url='http://pypi.python.org/pypi/SentryLogs/',
    license='LICENSE.txt',
    description='Send logs to Django Sentry.',
    long_description=open('README.md').read(),
    install_requires=[
        "raven >= 2.0.10",
        "tailer >= 0.3",
        ],
)