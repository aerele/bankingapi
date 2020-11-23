# -*- coding: utf-8 -*-
import banking_api

from setuptools import find_packages, setup
setup(
    name='banking_api',
    version= banking_api.__version__,
    description='Banking API Integration',
    author='Aerele',
    license='MIT',
    download_url='https://github.com/KaviyaPeriyasamy/bankingapi',
    author_email='admin@aerele.in',
    packages=['banking_api'],
    keywords=[
        'banking_api'
    ],
    python_requires='>=3.6'
)
