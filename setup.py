#!/usr/bin/env python

from distutils.core import setup

setup(name='tagswarm',
   version='1.0a1',
   description='File tagging utilities',
   author='Michel Albert',
   author_email='exhuma@foobar.lu',
   url='http://exhuma.github.com/tagswarm/',
   packages=['tagswarm'],
   scripts=['bin/cross_platform/tstag',
            'bin/cross_platform/tsuntag',
            'bin/cross_platform/tsdumbdialog.py',
            'bin/cross_platform/tsfastsearch']
   )

