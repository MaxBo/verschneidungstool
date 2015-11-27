# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from gui_hannover.control import MainWindow
import sys
from PyQt4 import QtGui
from gui_hannover.config import Config

config = Config()
config.read()

def startmain():

    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    startmain()