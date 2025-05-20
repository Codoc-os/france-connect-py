"""Setuptools entry point."""

import codecs
import os

from setuptools import setup

DIRNAME = os.path.dirname(__file__)
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
]
LONG_DESCRIPTION = (
    codecs.open(os.path.join(DIRNAME, 'README.md'), encoding='utf-8').read()
    + '\n'
    + codecs.open(os.path.join(DIRNAME, 'CHANGELOG.md'), encoding='utf-8').read()
)
REQUIREMENTS = [
    'pyjwt[crypto]>=2.9.0,<3.0.0',
    'requests>=2.32.3,<3.0.0',
]

setup(
    name='france-connect-py',
    version='2.1.0',
    description="A Python client to handle communication with FranceConnect",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Codoc',
    author_email='support@codoc.co',
    url='https://github.com/Codoc-os/france-connect-py',
    packages=['france_connect'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='MIT License',
    keywords='france-connect france-connect-py',
    classifiers=CLASSIFIERS,
)
