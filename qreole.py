#!/usr/bin/python
import sys
from PyQt4 import QtCore, QtGui
from main import MainWindow
app = QtGui.QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()
