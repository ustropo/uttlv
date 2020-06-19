#!/usr/bin/env python
import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# https://pythonhosted.org/an_example_pypi_project/setuptools.html#setting-up-setup-py
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='prtlv',
    version='0.2.2',
    description='Python library for TLV objects',
    long_description=read('README.md'),
    author='Prognosys - Sensing & Predicting',
    author_email='development@prognosys.com.br',
    license='MIT',
    packages=['prtlv'],
    install_requires=[],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT license',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)



