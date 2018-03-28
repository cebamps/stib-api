#!/bin/python3

from setuptools import setup

setup(
    name='stib_api',
    packages=['stib_api'],
    install_requires=[
        'requests',
        'requests_oauthlib',
        'oauthlib'
    ],
)
