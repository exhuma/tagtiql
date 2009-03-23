.. _command-line-tools:

Command Line Tools
==================

.. _tstag:

tstag - Basic tagger
--------------------

Tag one or many files (using standard globbing pattern) with one or many tags.

.. _shell-globbing:

*NOTE:* Depending on the shell behaviour you might need to enclose globbing
patterns in quotes. The application assumes that only the first parameters
specifies the filename pattern. Shells like ZSH expand the globbing pattern
BEFORE passing it to the application. This will cause only the first filename
to be tagged...... with the names of the other files as tags!

Usage::

   tstag <filename> <tag1> [tag2 [tag3 [tag4 ... ] ] ]


.. _tsuntag:

tsuntag - Tag remover
---------------------

Remove one or many tags from one or many files (using standard globbing pattern).

*NOTE:* The same note about specific shells applies to this tool.

Usage::

   tsuntag <filename> <tag1> [tag2 [tag3 [tag4 ... ] ] ]

.. _tsfastsearch:

tsfastsearch - Simple query tool
--------------------------------

Searches for files that have been tagged with *all* supplied tags.

Usage::

   tsfastsearch <tag1> [tag2 [tag3 [tag4 ... ] ] ]


