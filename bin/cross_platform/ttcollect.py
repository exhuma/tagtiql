#!/usr/bin/env python

import sys
from tagtiql.core import collect_tags
from os import getcwd
from os.path import abspath

root = getcwd()

if len(sys.argv) > 2:
   print """
Display all tags available in a given tree
If no starting folder is specified, it will take root at the current working
directory

Usage:
   %s [folder]
""" % sys.argv[0]
   sys.exit(1)

elif len(sys.argv) == 2:
   root = sys.argv[1]

print "Collecting tags. This may take a while..."
tag_collection = collect_tags( root )

# convert to a list of tuples
tag_collection = [ (x, tag_collection[x]) for x in tag_collection ]

# sort it
tag_collection.sort( cmp=lambda x,y: cmp(y[1], x[1]) )

print "-----------------------------------------------------------"
print "Available tags in %-40s:" % abspath(root)
print "-----------------------------------------------------------"
for row in tag_collection:
   print "%-35s was found %5d time(s)" % row
print "-----------------------------------------------------------"
