from Tkinter import *
from tkSimpleDialog import askstring
import sys
from tagswarm.core import fast_search

root = sys.argv[1]

master = Tk()
frame = Frame(master)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)
frame.pack(fill=BOTH, expand=1)

input = askstring("Tagtickle", "Enter a comma separated list of tags:", parent=frame)

if input:
    tags = [ x.strip() for x in input.split(',') ]
    searcher = fast_search( root, tags )
    for file_name in searcher:
        listbox.insert( END, file_name )

master.mainloop()
