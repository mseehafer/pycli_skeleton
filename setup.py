
import re
import os
import sys

from setuptools import setup, find_packages
#import unittest
from setuptools.command.test import test as TestCommand

PACKAGE = "clrtools"

INITFILE = open(os.path.join(os.path.dirname(__file__), PACKAGE, "__init__.py"))

VERSION = (
    re.compile(r""".*__version__ = ["'](.*?)["']""", re.S)
    .match(INITFILE.read())
    .group(1)
)
INITFILE.close()


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
        return f.read()


requires = [
    "SQLAlchemy>=0.9.0",
    "pandas"
]

# def my_test_suite():
#     test_loader = unittest.TestLoader()
#     test_suite = test_loader.discover('clrtools.tests', pattern='test_*.py')
#     return test_suite


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)



setup(name=PACKAGE,
      version=VERSION,
      description='Command Line Tool for CLR-DWH.',
      python_requires=">=3.5",
      long_description=readme(),
      #url='http://github.com/storborg/funniest',
      author='Flying Circus',
      #author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_packages(".", exclude=["examples*", "test*"]),
      tests_require=["pytest"],
      #test_suite='clrtools.tests.my_test_suite',
      cmdclass={"test": PyTest},
      zip_safe=False,
      install_requires=requires,
      entry_points = {
        'console_scripts': ['clrtools=clrtools.config:main'],
    })
