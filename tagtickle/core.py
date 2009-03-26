from sqlite3 import IntegrityError, OperationalError, connect
from os.path import abspath, dirname, join, exists, basename, isdir
from os import walk
import sys

DB_VERSION=2
IGNORED_FOLDERS = ['CVS', '.svn', '.git']
OP_ADD_TAG    = 1
OP_REMOVE_TAG = 2
SEARCH_CONJUNCTIVE = 1

def init_db(dbname):
    try:
       connection = connect( dbname )
    except OperationalError, ex:
       sys.stderr.write( "Unable to connect to the database %r. Errormessage was: %s\n" % ( dbname, str(ex) ) )
       return

    c = connection.cursor()
    c.execute('''CREATE TABLE file_tags(
        file_name text,
        tag text,
    PRIMARY KEY (file_name, tag))''')

    c.execute('''CREATE TABLE system(
        var text PRIMARY KEY,
        val text);''')

    # Let's store the DB revision number so we can ensure compatibility
    c.execute( 'INSERT INTO system (var, val) VALUES (?,?)', ('db_version', DB_VERSION) )

    connection.commit()
    c.close()

def tag_folder(root_folder, tags, op=OP_ADD_TAG):
    for root, dirs, files in walk(root_folder):
        for file in files:
            tag_path( join(root, file), tags, op )
        for ignored_folder in IGNORED_FOLDERS:
            if ignored_folder in dirs:
                dirs.remove(ignored_folder)  # don't visit CVS directories

def fast_search(root_folder, tags, op=SEARCH_CONJUNCTIVE):
    """
    Quickly search through the tags. This does not build a global tag index but
    instead queries tag-stores as it encounters them in the directory.

    It's implemented as a generator method. This alows on-the-fly search.
    """
    for root, dirs, files in walk(root_folder):
        for file in files:
            if file != "swarmtags.sqlite3":
                continue
            dbname = join( root, file )
            try:

                conn = connect( dbname )
            except OperationalError, ex: 
                sys.stderr.write( "Unable to connect to the database %r. Errormessage was: %s\n" % ( dbname, str(ex) ) )
                continue

            c = conn.cursor()

            subselects = [ "SELECT file_name FROM file_tags WHERE tag=?" for x in tags ]
            compound_q = " INTERSECT ".join( subselects )
            compound_q += " ORDER BY file_name"
            c.execute( compound_q, tags )

            for row in c:
                yield join( root, row[0] )

            c.close()
            conn.close()

def tag_path(path, tags, op=OP_ADD_TAG):

    if basename(path) == "swarmtags.sqlite3":
        # Avoid the tag DB itself to be tagged
        return

    if not exists(path):
        print "File %r not found" % path
        return

    # convert a string into a list of tags (splitting by commas)
    if isinstance(tags, basestring):
        tags = tags.split(",")

    # Clean up tags. Strip leading and trailing whitespace and remove duplicates.
    tags = set([ x.strip() for x in tags ])

    # if a tag is requested on a folder we will recurse into the folder and tag all files.
    if isdir(path):
       tag_folder(path, tags, op)
       return

    dbname = join( dirname( abspath( path ) ), 'swarmtags.sqlite3' )
    # initialise a non-existent DB
    #todo# This conditional might be put into the init_db method
    if not exists(dbname):
        init_db(dbname)

    try:
       conn = connect( dbname )
    except OperationalError, ex:
       sys.stderr.write( "Unable to connect to the database %r. Errormessage was: %s\n" % ( dbname, str(ex) ) )
       return None, None

    c = conn.cursor()

    for tag in tags:
        try:
            if op == OP_ADD_TAG:
               c.execute("INSERT INTO file_tags (file_name, tag) VALUES (?, ?)", (basename(path), tag))
            elif op == OP_REMOVE_TAG:
               c.execute("DELETE FROM file_tags WHERE file_name=? and tag=?", (basename(path), tag))
        except IntegrityError, ex:
            # duplicate entry
            pass
    conn.commit()
    c.close()
    return tags, dbname

def collect_tags(path):
    """
    Retrieves a list of tags available at a given location

    The paths are returned as a tuple containing the tag name and the number of
    ocurrences of that path
    """
    tags = {}
    for root, dirs, files in walk(path):
        # we only consider the tag store file for processing
        if "swarmtags.sqlite3" not in files:
            continue

        # if we came this far, we know that the tag store file is in the
        # current folder, so we can open it

        dbname = join( root, "swarmtags.sqlite3" )
        connection = None
        try:
           connection = connect( dbname )
        except OperationalError, ex:
           sys.stderr.write( "Unable to connect to the database %r. Errormessage was: %s\n" % ( dbname, str(ex) ) )
           return

        # connecting should have been successful at this point
        c = connection.cursor()
        c.execute( "SELECT tag, COUNT(*) FROM file_tags GROUP BY tag" )
        for tag, count in c:
            if tag not in tags:
                tags[tag] = count
            else:
                tags[tag] += count
        c.close()
        connection.close()

        # Next, we can remove the unwanted folders from the search
        for ignored_folder in IGNORED_FOLDERS:
            if ignored_folder in dirs:
                dirs.remove(ignored_folder)  # don't visit CVS directories

    return tags


if __name__ == "__main__":
    import sys
    op = int(sys.argv[2])
    if op not in [1,2]:
       raise ValueError("Operation must be either 1 (add tags) or 2 (remove tags)")
    tag_path(sys.argv[1], sys.argv[3:], op)
