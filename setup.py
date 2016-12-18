#!/usr/bin/env python

from distutils.core import setup

setup(
    name='semver',
    version='0.0.1',
    description='Semantic Versioning CLI tool and library',
    author='Phil Tysoe',
    author_email='philtysoe@gmail.com',
    url='https://github.com/igniteflow/semver',
    packages=['semver'],
    install_requires=[
        'mock',
    ],
    license='MIT',
    scripts=[
        'bin/semver'
    ],
)
