#!/usr/bin/env python

import sys
from os import walk, getcwd
from tagtickle.core import fast_search

if (len(sys.argv) < 2):
   print """
Tagswarm fast search
Find files having all of the specified tags

Usage:
   %s <tag1> [tag2 [tag3 [tag4 ... ] ] ]
""" % sys.argv[0]
   sys.exit(1)

searcher = fast_search( getcwd(), sys.argv[1:] )
for file_name in searcher:
   print file_name

