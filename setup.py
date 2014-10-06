# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import tournament_registration
version = tournament_registration.__version__

setup(
    name='tournament_registration_project',
    version=version,
    author='',
    author_email='eldruz@outlook.com',
    packages=[
        'tournament_registration',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['tournament_registration/manage.py'],
)