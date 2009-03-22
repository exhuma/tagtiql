import sqlite3
from hashlib import md5
from os.path import abspath, dirname, join, exists

DB_VERSION=1

def init_db(dbname):
    connection = sqlite3.connect( dbname )

    c = connection.cursor()
    c.execute('''CREATE TABLE file (
    hash text PRIMARY KEY,
    abspath text)''')
    
    c.execute('''CREATE TABLE file_tags(
        hash text REFERENCES file(hash) ON DELETE CASCADE,
        tag text, 
    PRIMARY KEY (hash, tag))''')
    
    c.execute('''CREATE TABLE system(
        var text PRIMARY KEY,
        val text);''')
    
    # Let's store the DB revision number so we can ensure compatibility
    c.execute( 'INSERT INTO system (var, val) VALUES (?,?)', ('db_version', DB_VERSION) )
    
    # Also keep the path of the tagged file, in order to detect swarmtag storage movements
    c.execute( 'INSERT INTO system (var, val) VALUES (?,?)', ('root_path', dirname( abspath( dbname ) )) )
    connection.commit()
    c.close()

def tag(filename, tags):
    dbname = join( dirname( abspath( filename ) ), 'swarmtags.sqlite3' )
    
    if not exists(filename):
        print "File not found"
        return

    if isinstance(tags, basestring):
        tags = tags.split(",")
    
    # what we want is a set of tags. not a list!
    # this remove duplicates as a side effect
    tags = set([ x.strip() for x in tags ])
    
    try:
        hash = md5( open(filename).read() ).hexdigest()
    except IOError, ex:
        print "Unable to open file '%s' for hashing. Aborting..." % filename
        raise

    # initialise a non-existent DB
    if not exists(dbname):
        init_db(dbname)

    conn = sqlite3.connect( dbname )
    c = conn.cursor()

    try:
        c.execute("INSERT INTO file (hash, abspath) VALUES (?, ?)",
            (hash, abspath(filename)))
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

if __name__ == "__main__":
    import sys
    tag(sys.argv[1], sys.argv[2:])