#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
import os

class BrowserWindow(QDialog):
    def __init__(self, notesPath, curDir, parent=None):
	QDialog.__init__(self)
	uic.loadUi("browser.ui", self)
	self.setWindowTitle('Wiki Browser')
	self.parent = parent
	self.buttonOpen = QPushButton("&Open file");
	self.buttonOpen.setDefault(True)
	self.buttonNewFile = QPushButton("&New file");
	self.buttonNewFolder = QPushButton("New &folder");
	self.buttonDelete = QPushButton("&Remove");
	self.buttonClose = QPushButton("&Close");
	self.buttonBox.addButton(self.buttonOpen, QDialogButtonBox.AcceptRole)
	self.buttonBox.addButton(self.buttonNewFile, QDialogButtonBox.ActionRole)
	self.buttonBox.addButton(self.buttonNewFolder, QDialogButtonBox.ActionRole)
	self.buttonBox.addButton(self.buttonDelete, QDialogButtonBox.ActionRole)
	self.buttonBox.addButton(self.buttonClose, QDialogButtonBox.RejectRole)
	self.connect(self.buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
	self.connect(self.buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
	self.notesPath = notesPath
	self.model = QFileSystemModel()
	self.model.setRootPath(notesPath)
	self.model.setNameFilters(['*.txt'])
	self.model.setNameFilterDisables(False)
	self.treeView.setModel(self.model)
	self.treeView.setRootIndex(self.model.index(notesPath))
	self.treeView.header().setResizeMode(QHeaderView.ResizeToContents)
	self.treeView.setExpandsOnDoubleClick(True)
	self.connect(self.treeView, SIGNAL("doubleClicked(const QModelIndex&)"), self.doubleClick)
	self.connect(self.buttonNewFolder, SIGNAL("clicked()"), self.mkDir)
	self.connect(self.buttonDelete, SIGNAL("clicked()"), self.rmDir)
	self.connect(self.buttonNewFile, SIGNAL("clicked()"), self.newNote)
	print 'NOTES DIR:', notesPath
	print 'CUR DIR:', curDir
	self.selectItem(curDir)

    def selected(self):
	sel = self.treeView.selectedIndexes()
	if sel:
	    return sel[0]
	return self.treeView.rootIndex()

    def fileName(self):
	sel = self.selected()
	if sel:
	    return unicode(self.model.filePath(self.selected())[len(self.notesPath):])
	else:
	    return u'/'

    def doubleClick(self):
    	if self.selected() and not self.model.isDir(self.selected()):
	    self.accept()

    def selectItem(self, search):
	idx0 = self.model.index(search, 0)
	idx1 = self.model.index(search, self.model.columnCount() - 1)
	assert idx0.isValid(), idx1.isValid()
	self.treeView.selectionModel().select(QItemSelection(idx0, idx1), QItemSelectionModel.ClearAndSelect)
	self.treeView.scrollTo(idx0)

    def newNote(self):
	fname = self.getFName('New Note', 'Note Name:')
	if fname is not None:
	    path = self.getPath()
	    print 'NEW NOTE:', path, fname
	    self.mkNote(os.path.join(path, fname))
	    self.selectItem(os.path.join(path, fname) + '.txt')
	    self.accept()

    def mkNote(self, path):
	f = open(path+'.txt', 'w')
	f.close()

    def getPath(self):
	sel = self.selected()
	if sel:
	    path = unicode(self.model.filePath(sel))
	    if not os.path.isdir(path):
		path = os.path.split(path)[0]
	else:
	    path = self.notesPath
	return path

    def mkDir(self):
	folder = self.getFName('New Folder', 'Folder Name:')
	if folder is not None:
	    path = os.path.join(self.getPath(), folder)
	    print path
	    os.mkdir(path)

    def rmDir(self):
	from shutil import rmtree
	sel = self.selected()
	if sel:
	    path = unicode(self.model.filePath(sel))
	    fname = self.fileName()
	    isdir = os.path.isdir(path)
	    if isdir: s = 'folder'
	    else: s = 'note'
	    ans = QMessageBox.question(self, "Removing", "You're going to permanently remove the %s<br/>%s.<br/>Are you sure?" % (s, fname), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
	    if ans == QMessageBox.Yes:
		print "REMOVING", path
		if isdir:
		    rmtree(path)
		else:
		    os.unlink(path)
	else:
	    QMessageBox.warning(self, "Removing", "Nothing to remove.<br/>Select note/folder first!")

    def getFName(self, caption, prompt):
	answer, ok = QInputDialog.getText(self, caption, prompt, QLineEdit.Normal, "")
	if ok and answer:
	    return unicode(answer)
	return None
