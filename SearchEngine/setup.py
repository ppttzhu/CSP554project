#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(install_requires=requirements)
