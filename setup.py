from glob import glob
from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa N812
from shlex import split
from shutil import rmtree
from os import remove
from os.path import abspath, dirname, join

import sentrylogs as package


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline
        args = self.tox_args
        if args:
            args = split(self.tox_args)
        errno = cmdline(args=args)
        exit(errno)


class Clean(TestCommand):
    def run(self):
        delete_in_root = [
            'build',
            'dist',
            '.eggs',
            '*.egg-info',
            '.tox',
        ]
        delete_everywhere = [
            '__pycache__',
            '*.pyc',
        ]
        for candidate in delete_in_root:
            rmtree_glob(candidate)
        for visible_dir in glob('[A-Za-z0-9]*'):
            for candidate in delete_everywhere:
                rmtree_glob(join(visible_dir, candidate))
                rmtree_glob(join(visible_dir, '*', candidate))
                rmtree_glob(join(visible_dir, '*', '*', candidate))


def rmtree_glob(file_glob):
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
    with open(join(abspath(dirname(__file__)), filename)) as f:
        return f.read()


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
