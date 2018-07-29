#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='chat-web',
    version='0.0.1',
    include_package_data=True,
    packages=find_packages(exclude=['doc', 'tests*']),
    install_requires=[
        'aiohttp',
        'aiohttp_session',
        'cryptography',
        'cchardet',
        'aiodns',
        'requests_oauthlib',
    ],
    entry_points={
        'console_scripts': [
            'chat-web=chat_web:chat_web_main',
        ],
    })
