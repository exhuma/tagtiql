from Tkinter import Tk
from tkSimpleDialog import askstring
import sys
import tagswarm

filename = sys.argv[1]

root = Tk()
root.withdraw()

input = askstring("Swarmtags", "Enter a comma separated list of tags:")

if input:
    tags, tagfile = tagswarm.tag( filename, input )
