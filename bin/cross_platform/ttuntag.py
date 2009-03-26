#!/usr/bin/env python

import sys
from glob import glob
from tagtickle.core import tag_path, OP_REMOVE_TAG

if (len(sys.argv) < 3):
   print """
Tagswarm un-tagger.
Remove one or many tags from one or many files (using standard globbing pattern).

NOTE: Depending on the shell behaviour you might need to enclose globbing
patterns in quotes. The application assumes that only the first parameters
specifies the filename pattern. Shells like ZSH expand the globbing pattern
BEFORE passing it to the application. This will cause only the first filename
to be tagged...... with the names of the other files as tags!

Usage:
   %s <filename> <tag1> [tag2 [tag3 [tag4 ... ] ] ]
""" % sys.argv[0]
   sys.exit(1)

for path in glob(sys.argv[1]):
   tag_path( path, sys.argv[2:], OP_REMOVE_TAG )

