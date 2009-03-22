tagswarm
========

Contents
--------
  .. toctree::
     :maxdepth: 2

Description
===========

I felt like writing a small tool to tag files and make thoes tags easily
available. The currently available tools (at least those I found) feel too much
like sledgehammers.

Motivations
-----------

   * Make tagging dead-simple (windows shell integration, command-line)
   * If a file is tagged in one OS, this tag should be usable in other OSes
   * Don't rely on a central database, keep the tags as close as possible to the files

Design decisions
----------------

   * Store the tags in a reusable and flexible file-format --> SQLite3
   * Store this file in the same folder as the files themseves (similar to
     thumbs.db)

        * Distributed storage decreases the loss of data
        * If a folder with files are deleted, all attached tags are gone as well.
        * retrieving the tags becomes more complicated

   * Store as little information about the files as possible. But enough to be
     able to identify them (filename, tag)
   * Don't give the tags any numeric IDs. Use their name as natural key (makes
     merging the distributed tag files trivial but increases storage volume)

*BE WARNED:*
This is in a very early stage of development. I develop it in first line for
myself. I do not care about performance and such... at least not for now. I
dunno how well it will perform on millions of files. But that's out of the
scope of my need anyhow. As it is right now, tagging and un-tagging seems to
work well. If files are renamed, there tags are obviously lost. That's not
easily detectable.  Hashing the files also won't work as the contents of the
files are usually subject to change.

Searching in the created tag-indexes is non-trivial as one needs to collect all
tags from all tag-container-files before searching. For large file-sets (think
of subdirectories) this may kill resources (memory or disk-space depending on
how it's implemented). Again, that's out of scope of my needs.

As of now, I've finished the most basic operations for tagging. I probably
won't get a lot of time to get more work done over the forseeable future. But
eventually I will fool around a bit more. Until then, have fun... or not....
with this toy

As usually with OSS, if anyone happens to create a solution for browsing the
tag-"swarms", feel free to let me know

Dependencies
------------

If you are using Python >= 2.6 then you are fine. If it's Python <2.6 than you
need to install pysqlite3.

Install
-------

Nothing to install. Clone it and you are ready to rock. With a small exception.
I added a small windows .reg file which can be imported to enable the shell
integration. Before you do that though, have a look at it and replace the path
names with the correct ones!

License
-------

LGPL

Download
--------

You can download this project in either
`zip <http://github.com/exhuma/tagswarm/zipball/master>`_ or
`tar <http://github.com/exhuma/tagswarm/tarball/master>`_ formats.

You can also clone the project with `Git <http://git-scm.com/>`_ by running::

   $ git clone git://github.com/exhuma/tagswarm

.. Welcome to tagswarm's documentation!
   ====================================
   Contents:
   .. toctree::
      :maxdepth: 2
   Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

