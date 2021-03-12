# -*- coding: utf-8 -*-
import banking_api

from setuptools import find_packages, setup
with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')
setup(
    name='banking_api',
    version= banking_api.__version__,
    description='Banking API Integration',
    author='Aerele',
    license='MIT',
    download_url='https://github.com/aerele/bankingapi',
    author_email='admin@aerele.in',
    packages=['banking_api'],
    keywords=[
        'banking_api'
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)
