#!/usr/bin/env python
from Tkinter import Tk
from tkSimpleDialog import askstring
import sys
from tagswarm.core import tag_path

filename = sys.argv[1]

root = Tk()
#root.withdraw()

input = askstring("Swarmtags", "Enter a comma separated list of tags:")

if input:
    tags, tagfile = tag_path( filename, input )

