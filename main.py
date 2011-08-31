#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from creoleparser import creole2html
import os.path
from editor import EditWindow
from browser import BrowserWindow
from utils import SimpleConfig

VERSION = '0.3'

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
	self.connect(self.action_Back, SIGNAL("triggered()"),
		     self.goBack)
	self.connect(self.action_Refresh, SIGNAL("triggered()"),
		     self.reloadNote)
	self.notesDir = self.config.readStr('WikiDir')
	if self.notesDir.endswith('/'):
	    self.notesDir = self.notesDir[:-1]
	self.history = list()
	self._currentFile = None
	self.homePage = self.config.readStr('HomePage')
	if not self.homePage.startswith('/'):
	    self.homePage = '/' + self.homePage
	print self.notesDir, self.homePage
	self.Browser.setSearchPaths(['.', self.notesDir, self.config.readStr('ImageDir')])
	self.goHome()

    def get_currentNote(self):
	if self._currentFile:
	    value = self._currentFile[len(self.notesDir):]
	    print '**** CURRENTNOTE:', value
	    return value
	else:
	    return None

    def get_fileName(self):
	if self._currentFile:
	    return self._currentFile + '.txt'

    fileName = property(get_fileName)

    def set_currentNote(self, value):
	if value.startswith('/'):
	    value = os.path.join(self.notesDir, value[1:])
	else:
	    value = os.path.realpath(os.path.join(self.currentDir, value))
	self._currentFile = value
	print '**** CURRENTFILE SET:', self._currentFile

    currentNote = property(get_currentNote, set_currentNote)

    def get_currentDir(self):
	path = os.path.split(self._currentFile)[0]
	return path

    currentDir = property(get_currentDir)

    def _getText(self):
	try:
	    return open(self.fileName, 'r').read().decode('utf-8')
	except IOError:
	    return None

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

    def browseNotes(self):
	print "BROWSE"
	dlg = BrowserWindow(self.notesDir, self.currentDir, self)
	if dlg.exec_():
	    fileName = dlg.fileName()
	    print '    SELECTED:', repr(fileName)
	    self.open(os.path.splitext(fileName)[0])

    def followLink(self, link):
	note = unicode(link.toString())
	print 'CLICKED:', note
	self.open(note)

    def goHome(self):
	self.open(self.homePage)

    def goBack(self):
	print 'BACK:'
	try:
	    last = self.history.pop()
	except IndexError:
	    return
	print '     ', last
	self.open(last, True)

    def reloadNote(self):
	self.open(back=True)

    def open(self, fileName=None, back=False):
	print '=== OPEN'
	if self.currentNote and not back:
	    if (not self.history) or (self.history and self.history[-1] != self.currentNote):
		self.history.append(self.currentNote)
	print 'HISTORY:'
	print '   ', '\n    '.join(self.history)
	if fileName:
	    self.currentNote = fileName
	txt = self._getText()
	if not txt:		# new note
	    self.editNote()
	else:
	    html = creole2html.render(txt).decode('utf-8')
#	    self.TMP_SaveHtml(html)
	    self.Browser.setHtml(html)
	    self.updateTitle()

    def save(self, txt):
	f = open(self.fileName, 'w')
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

    def TMP_SaveHtml(self, html):
	if self.currentNote.startswith('/'):
	    path = os.path.join(self.notesDir, self.currentNote[1:])
	else:
	    path = os.path.realpath(os.path.join(self.notesDir, self.currentDir, self.currentNote))
	f = open(path + '.html', 'w')
	f.write(html.encode('utf-8'))
	f.close()

