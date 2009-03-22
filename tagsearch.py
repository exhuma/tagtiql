from ui.main_window import Ui_MainWindow
from PyQt4 import QtGui
import sys
from os import walk, getcwd
from os.path import join, exists
from tagswarm import init_db
from sqlite3 import connect

def collect_tags():
   """
   Construct or update an accumulated index of all known files and tags.
   """
   swarm_files = []
   for root, dirs, files in walk( getcwd() ):
      for file in files:
         if file == "swarmtags.sqlite3":
            swarm_files.append( join( root, file ) )

   localcache = "swarm_cache.sqlite3"
   #todo# This conditional might be put into the init_db method
   if not exists(localcache):
      init_db(localcache)

   conn = connect( localcache )
   c = conn.cursor()

   for tag_file in swarm_files:
      tmpconn = connect( tag_file )
      c2 = tmpconn.cursor()
      c2.execute("SELECT * FROM file_tags")
      c2.close()
      tmpconn.close()

   c.close()
   conn.close()

class MainWindow(QtGui.QMainWindow):
   def __init__(self, parent=None):
      QtGui.QWidget.__init__(self, parent)
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)

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

