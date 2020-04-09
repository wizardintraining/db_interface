#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from io import open
import sys

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'db_interface'
DESCRIPTION = 'Adds DB interface to pull model data from'
URL = ''
EMAIL = 'stewhite@redhat.com'
AUTHOR = 'Stephone White'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

REQUIRED = [
        'flask',
        'sqlalchemy',
        ]
EXTRAS = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
        }

here = path.abspath(path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={ NAME: 'src'},
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    # include_package_data=True,
    license='BSD',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
