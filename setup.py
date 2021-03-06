#!/usr/bin/env python3

from distutils.core import setup

setup(name='Cadmus',
      version='0.1.0',
      description='A LaTeX front-end to Sphinx',
      author='Marcus Eriksson',
      author_email='marcus.jr.eriksson@gmail.com',
      packages=['cadmus',
                'cadmus.doc',
                'cadmus.fig',
                'cadmus.fig.templates'])
