#!/usr/bin/env python
from Tkinter import *
from tkSimpleDialog import askstring
import sys
from tagtickle.core import fast_search

root = sys.argv[1]

def do_search(event):
    input = event.widget.get()
    listbox.delete(0, END)
    if input:
        tags = [ x.strip() for x in input.split(',') ]
        searcher = fast_search( root, tags )
        for file_name in searcher:
            listbox.insert( END, file_name )

master = Tk()
frame = Frame(master)
txtInput = Entry(frame)
txtInput.pack(side=TOP, fill=X)
txtInput.focus_set()
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)
frame.pack(fill=BOTH, expand=1)

txtInput.bind("<Return>", do_search)

master.mainloop()
