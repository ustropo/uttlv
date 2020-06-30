#!/usr/bin/env python
import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='uttlv',
    version='0.4.0',
    description='Python library for TLV objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ustropo/uttlv',
    download_url='https://github.com/ustropo/uttlv/archive/v0.4.0.tar.gz',
    author='Fernando C. de Souza',
    author_email='cleberdsouza@gmail.com',
    license='MIT',
    packages=['uttlv'],
    install_requires=[],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)



