#!/usr/bin/env python

from distutils.core import setup

setup(name='Cadmus',
      version='0.1',
      description='A LaTeX front-end to Sphinx',
      author='Marcus Eriksson',
      author_email='marcus.jr.eriksson@gmail.com',
      packages=['cadmus',
                'cadmus.doc',
                'cadmus.fig',
                'cadmus.fig.templates'])
