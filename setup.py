#!/usr/bin/env python

from distutils.core import setup

setup(name='tagtickle',
   version='1.0a1',
   description='File tagging utilities',
   author='Michel Albert',
   author_email='exhuma@foobar.lu',
   url='http://exhuma.github.com/tagswarm/',
   packages=['tagtickle'],
   scripts=[
      'bin/cross_platform/tkttfind.py',
      'bin/cross_platform/tktttag.py',
      'bin/cross_platform/ttquery.py',
      'bin/cross_platform/tttag.py',
      'bin/cross_platform/ttcollect.py',
      'bin/cross_platform/ttuntag.py',
      ]
   )

