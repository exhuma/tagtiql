from sqlite3 import IntegrityError, OperationalError, connect
from os.path import abspath, dirname, join, exists, basename, isdir
from os import walk
import sys

DB_VERSION=2
IGNORED_FOLDERS = ['CVS', '.svn', '.git']
OP_ADD_TAG    = 1
OP_REMOVE_TAG = 2

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

if __name__ == "__main__":
    import sys
    op = int(sys.argv[2])
    if op not in [1,2]:
       raise ValueError("Operation must be either 1 (add tags) or 2 (remove tags)")
    tag_path(sys.argv[1], sys.argv[3:], op)
