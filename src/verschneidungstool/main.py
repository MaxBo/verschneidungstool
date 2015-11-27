# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from verschneidungstool.control import MainWindow
import sys
from PyQt4 import QtGui
from verschneidungstool.config import Config

config = Config()
config.read()

def startmain():

    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    startmain()