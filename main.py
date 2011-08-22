#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from creoleparser import creole2html
import os.path
from editor import EditWindow
from browser import BrowserWindow
from utils import SimpleConfig

VERSION = '0.2'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
	self.config = SimpleConfig('~/.qreolerc')
	QMainWindow.__init__(self)
	uic.loadUi("main.ui", self)
	self.connect(self.action_Exit, SIGNAL("triggered()"),
		     qApp, SLOT("quit()"))
	self.connect(self.action_About, SIGNAL("triggered()"),
		     self.showAboutBox)
	self.connect(self.actionBrowse, SIGNAL("triggered()"),
		     self.browseNotes)
	self.connect(self.Browser, SIGNAL("anchorClicked(const QUrl&)"), 
		     self.followLink)
	self.connect(self.action_Edit, SIGNAL("triggered()"),
		     self.editNote)
	self.connect(self.actionHome, SIGNAL("triggered()"),
		     self.goHome)
	self.notesDir = self.config.readStr('WikiDir')
	self.currentDir = ''
	self.homePage = self.config.readStr('HomePage')
	if not self.homePage.startswith('/'):
	    self.homePage = '/' + self.homePage
	print self.notesDir, self.homePage
	self.Browser.setSearchPaths(['.', self.notesDir, self.config.readStr('ImageDir')])
	self.open(self.homePage)

    def updateTitle(self):
	title = 'Qreole %s' % VERSION
	if self.currentNote:
	    title += ' - %s' % self.currentNote
	self.setWindowTitle(title)

    def showAboutBox(self):
        QMessageBox.about(self, "About",
                          "<h2>Qreole</h2>" +
                          """<p>Personal Wiki with Creole markup</p>
<p>Version %s</p>
<p>&copy; Dmitri Brechalov, 2011</p>""" % VERSION)

    def _getFileName(self):
	if self.currentNote.startswith('/'):
	    path = os.path.join(self.notesDir, self.currentNote[1:])
	else:
	    path = os.path.realpath(os.path.join(self.notesDir, self.currentDir, self.currentNote))
	self.currentDir = os.path.dirname(path)
	self.currentNote = os.path.basename(path)
	print 'PATH:', path
	print 'DIR:', self.currentDir
	print 'NOTE:', self.currentNote
	return  path + '.txt'
    
    def browseNotes(self):
	print "BROWSE"
	dlg = BrowserWindow(self.notesDir)
	if dlg.exec_():
	    fileName = unicode(dlg.fileName())
	    print '    SELECTED:', repr(fileName)
	    self.open(os.path.splitext(fileName)[0])

    def followLink(self, link):
	self.currentNote = unicode(link.toString())
	print 'CLICKED:', self.currentNote
	self.open()

    def _getText(self):
	try:
	    return open(self._getFileName(), 'r').read().decode('utf-8')
	except IOError:
	    return None

    def TMP_SaveHtml(self, html):
	if self.currentNote.startswith('/'):
	    path = os.path.join(self.notesDir, self.currentNote[1:])
	else:
	    path = os.path.realpath(os.path.join(self.notesDir, self.currentDir, self.currentNote))
	f = open(path + '.html', 'w')
	f.write(html.encode('utf-8'))
	f.close()

    def open(self, fileName=None):
	if fileName:
	    self.currentNote = fileName
	txt = self._getText()
	if txt is None:		# new note
	    self.editNote()
	else:
	    html = creole2html.render(txt).decode('utf-8')
#	    self.TMP_SaveHtml(html)
	    self.Browser.setHtml(html)
	    self.updateTitle()

    def save(self, txt):
	f = open(self._getFileName(), 'w')
	f.write(txt)
	f.close()

    def editNote(self):
	dlg = EditWindow(self.currentNote)
	txt = self._getText()
	if txt:
	    dlg.TextEditor.setPlainText(txt)
	if dlg.exec_():
	    print "OK PRESSED"
	    txt = unicode(dlg.TextEditor.toPlainText()).encode('utf-8')
	    self.save(txt)
	    self.open()

    def goHome(self):
	self.open(self.homePage)
