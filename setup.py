#!/usr/bin/env python

from setuptools import setup

setup(
    name='thekevincrane',
    version='0.0.1',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['pip', 'Flask']
)
