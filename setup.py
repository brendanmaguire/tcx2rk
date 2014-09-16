#!/usr/bin/env python

import os
import sys

# Sets __version__
execfile('tcx2rk/_version.py')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

try:
    import pypandoc
    description = pypandoc.convert('README.markdown', 'rst')
except (IOError, ImportError):
    description = ''

requires = [
    'argh==0.24.1',
    'argcomplete==0.8.1',
    'xmltodict==0.8.6',
]

setup(
    name='tcx2rk',
    version=__version__,
    description='Convert TCX files to the Runkeeper format',
    long_description=description,
    author='Brendan Maguire',
    author_email='maguire.brendan@gmail.com',
    install_requires=requires,
    license='Apache 2.0',
    scripts=['bin/tcx2rk'],
    url='https://github.com/brendanmaguire/tcx2rk',
    packages=['tcx2rk'],
)
