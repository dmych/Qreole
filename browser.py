#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class BrowserWindow(QDialog):
    def __init__(self, NotesPath, parent=None):
	QDialog.__init__(self)
	uic.loadUi("browser.ui", self)
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
	self.notesPath = NotesPath
	self.model = QFileSystemModel()
	self.model.setRootPath(NotesPath)
	self.model.setNameFilters(['*.txt'])
	self.model.setNameFilterDisables(False)
	self.treeView.setModel(self.model)
	self.treeView.setRootIndex(self.model.index(NotesPath))
	self.treeView.header().setResizeMode(QHeaderView.ResizeToContents)
	self.treeView.setExpandsOnDoubleClick(True)
#	self.connect(self.treeView, SIGNAL("doubleClicked(const QModelIndex&)"), self, SLOT("accept()"))
#	self.connect(self.treeView, SIGNAL("doubleClicked(const QModelIndex&)"), self.doubleClick)
	print 'DIR:', NotesPath

    def selected(self):
	return self.treeView.selectedIndexes()[0]

    def fileName(self):
	return self.model.filePath(self.selected())[len(self.notesPath):]

    # def doubleClick(self):
    # 	if self.model.isDir(self.selected()):
    # 	    self.
