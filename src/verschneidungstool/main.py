# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from verschneidungstool.control import MainWindow
import sys
from PyQt4 import QtGui
from verschneidungstool.config import Config

config = Config()
config.read()

def startmain():

    parser = ArgumentParser(description="GUI Verschneidungstool")

    parser.add_argument("-config", action="store_true",
                        help="Pfad zu einer XML-Config-Datei mit den Verbindungsdaten und Pfaden zu den Postgres-Tools (optional)",
                        dest="config")

    parser.add_argument("-upload", action="store_true",
                        help="Shapefile hochladen (optional)",
                        dest="upload")

    parser.add_argument("-pfad", action="store",
                        help="Pfad zum Shapefile (Pflicht bei Shapefile-Upload)",
                        dest="shape_path")

    parser.add_argument("-schema", action="store",
                        help="Zielschema in der Datenbank (Pflicht bei Shapefile-Upload)",
                        dest="scheme")

    parser.add_argument("-name", action="store",
                        help="Name der zu erzeugenden Tabelle in der Datenbank (optional bei Shapefile-Upload)",
                        dest="table_name")

    parser.add_argument("-srid", action="store",
                        help="Projektion des Shapefiles bei Shapefile-Upload (optional bei Shapefile-Upload)",
                        dest="srid")

    parser.add_argument("-gebiet_id", action="store",
                        help="Spalte für ID bei Shapefile-Upload (optional bei Shapefile-Upload)",
                        dest="c_id")

    parser.add_argument("-gebiet_name", action="store",
                        help="Spalte mit Gebietsnamen bei Shapefile-Upload (optional bei Shapefile-Upload)",
                        dest="c_name")

    #parser.add_argument("-shape", action="store",
                        #help="shapefile hochladen",
                        #dest="shape_file", default=None)

    #parser.add_argument("-shape", action="store",
                        #help="shapefile hochladen",
                        #dest="shape_file", default=None)

    #parser.add_argument("-run", action="store",
                        #help="angegebenes Szenario ausführen",
                        #dest="scenario_name", default=None)

    arguments = parser.parse_args()

    upload = arguments.upload
    shape_path = arguments.shape_path
    scheme = arguments.scheme

    if upload and (not shape_path or not scheme):
        print('Um ein Shapefile hochzuladen, müssen Pfad zum Shapefile und Zielschema angegeben werden.')
        exit(1)

    if upload and (not shape_path or not scheme):
        print('Um ein Shapefile hochzuladen, müssen Pfad')
        exit(1)

    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.exec_arguments(arguments)
    sys.exit(app.exec_())

if __name__ == "__main__":
    startmain()
