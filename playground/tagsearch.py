from ui.main_window import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import sys
from os import walk, getcwd
from os.path import join, exists, dirname
from tagtiql import init_db
from sqlite3 import connect, IntegrityError
LOCALCACHE = "swarm_cache.sqlite3"

def collect_tags():
   """
   Construct or update an accumulated index of all known files and tags.
   """
   swarm_files = []
   for root, dirs, files in walk( getcwd() ):
      for file in files:
         if file == "swarmtags.sqlite3":
            swarm_files.append( join( root, file ) )

   #todo# This conditional might be put into the init_db method
   if not exists(LOCALCACHE):
      init_db(LOCALCACHE)

   #todo# The local cache might well be stored in the user's app-data/home folder. Risk of running out of disk-space though!
   conn = connect( LOCALCACHE )

   c = conn.cursor()

   for tag_file in swarm_files:
      tmpconn = connect( tag_file )
      c2 = tmpconn.cursor()
      c2.execute("SELECT * FROM file_tags")
      tag_file_dir = dirname(tag_file)
      for row in c2:
         try:
            c.execute( "INSERT INTO file_tags (file_name, tag) VALUES (?, ?)", [join(tag_file_dir, row[0]), row[1]] )
         except IntegrityError, ex:
            # duplicate entry
            pass
      c2.close()
      tmpconn.close()

   conn.commit()
   c.close()

class MainWindow(QtGui.QMainWindow):

   def __init__(self, parent=None):
      QtGui.QWidget.__init__(self, parent)
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)

      QtCore.QObject.connect(self.ui.lstTags, QtCore.SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'), self.update_filelist )

      self.update_taglist()

   ##@QtCore.pyqtSignature("on_lstTags_clicked()")
   def update_filelist(self, item, previous):
      conn = connect( LOCALCACHE )
      c = conn.cursor()
      tag = str(item.data(QtCore.Qt.UserRole).toString())
      self.ui.lstFiles.clear()
      q = "SELECT file_name FROM file_tags WHERE tag=?"
      c.execute(q, [tag])
      for row in c:
         item = QtGui.QListWidgetItem( "%s" % row[0], self.ui.lstFiles )
      c.close()
      conn.close()


   def update_taglist(self, parent_tags=None):
      """
      Update the list of tags in the UI.
      If parent_tags are specified only show tags that are attached to files also
      having all the parent tags
      """
      conn = connect( LOCALCACHE )
      self.ui.lstTags.clear()

      c = conn.cursor()
      if parent_tags:
         subselects = [ "SELECT file_name FROM file_tags WHERE tag=?" for x in parent_tags ]
         subq = " INTERSECT ".join( subselects )
         q = "SELECT tag, COUNT(*) FROM file_tags WHERE file_name IN ("+subq+") GROUP BY tag ORDER BY COUNT(*) DESC"
         c.execute( q, parent_tags )
      else:
         q = "SELECT tag, COUNT(*) FROM file_tags GROUP BY tag ORDER BY COUNT(*) DESC"
         c.execute( q )

      for row in c:
         item = QtGui.QListWidgetItem( "%s (%d)" % row, self.ui.lstTags )
         item.setData( QtCore.Qt.UserRole, QtCore.QVariant(row[0]) )

      c.close()


if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)

   dw = app.desktop().width()
   dh = app.desktop().height()

   myapp = MainWindow()
   myapp.setGeometry(
         int((dw - (dw - (dw / 2)) * 1.5) / 2),
         int((dh - (dh - (dh / 2)) * 1.5) / 2),
         int((dw - (dw / 2)) * 1.5),
         int((dh - (dh / 2)) * 1.5))
   myapp.show()

   collect_tags()
   sys.exit(app.exec_())

