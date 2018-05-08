#!/usr/bin/env python
"""Flashfact project"""
from setuptools import find_packages, setup

setup(name = 'flashfact',
    version = '0.1',
    description = "Flash Fact.",
    long_description = "Event processor.",
    platforms = ["Linux"],
    author="Pete Moore",
    author_email="1petemoore@gmail.com",
    url="https://pymbook.readthedocs.io/en/latest/",
    license = "MIT",
    packages=find_packages()
    )