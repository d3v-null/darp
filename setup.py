#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Setup module """

import os
import re
from setuptools import setup, find_packages

# Get version from __init__.py file
VERSION = ""
with open("darp/__init__.py", "r") as fd:
    VERSION = re.search(r"^__version__\s*=\s*['\"]([^\"]*)['\"]", fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError("Cannot find version information")

# Get long description
with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="darp",
    version=VERSION,
    description="A Python utility to detect devices joining or leaving the local network",
    long_description=README,
    author="Derwent McElhinney @ Laserphile",
    author_email="derwent@laserphile.com",
    url="https://github.com/derwentx/darp",
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=(
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Networking :: Monitoring"
    ),
)
