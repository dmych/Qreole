#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class EditWindow(QDialog):
    def __init__(self, title, parent=None):
	QDialog.__init__(self)
	uic.loadUi("editor.ui", self)
	self.setWindowTitle('Edit: %s' % title)
