from sqlite3 import IntegrityError, connect
from hashlib import md5
from os.path import abspath, dirname, join, exists, basename, isdir
from os import walk

DB_VERSION=1

IGNORED_FOLDERS = ['CVS', '.svn', '.git']

def init_db(dbname):
    connection = connect( dbname )

    c = connection.cursor()
    c.execute('''CREATE TABLE file (
    hash text PRIMARY KEY,
    name text)''')

    c.execute('''CREATE TABLE file_tags(
        hash text REFERENCES file(hash) ON DELETE CASCADE,
        tag text,
    PRIMARY KEY (hash, tag))''')

    c.execute('''CREATE TABLE system(
        var text PRIMARY KEY,
        val text);''')

    # Let's store the DB revision number so we can ensure compatibility
    c.execute( 'INSERT INTO system (var, val) VALUES (?,?)', ('db_version', DB_VERSION) )

    connection.commit()
    c.close()

def tag_folder(root_folder, tags):
    for root, dirs, files in walk(root_folder):
        for file in files:
            add_tags( join(root, file), tags )
        for ignored_folder in IGNORED_FOLDERS:
            if ignored_folder in dirs:
                dirs.remove(ignored_folder)  # don't visit CVS directories

def add_tags(path, tags):

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
       tag_folder(path, tags)
       return

    try:
        hash = md5( open(path).read() ).hexdigest()
    except IOError, ex:
        print "Unable to open file '%s' for hashing. Aborting..." % path
        raise

    dbname = join( dirname( abspath( path ) ), 'swarmtags.sqlite3' )
    # initialise a non-existent DB
    if not exists(dbname):
        init_db(dbname)

    conn = connect( dbname )
    c = conn.cursor()

    try:
        c.execute("INSERT INTO file (hash, name) VALUES (?, ?)",
            (hash, basename(path)))
    except IntegrityError, ex:
        # duplicate entry
        pass

    for tag in tags:
        try:
            c.execute("INSERT INTO file_tags (hash, tag) VALUES (?, ?)", (hash, tag))
        except IntegrityError, ex:
            # duplicate entry
            pass
    conn.commit()
    c.close()
    return tags, dbname

if __name__ == "__main__":
    import sys
    add_tags(sys.argv[1], sys.argv[2:])
