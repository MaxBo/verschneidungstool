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
                        help="Shapefile hochladen",
                        dest="upload")

    parser.add_argument("-verschneiden", action="store_true",
                        help="Verschneidung durchführen",
                        dest="intersection")

    parser.add_argument("-download", action="store_true",
                        help="Ergebnisse herunterladen",
                        dest="download")

    parser.add_argument("-shapefile", action="store",
                        help="Pfad zur Datei (Pflicht bei Shapefile-Upload)",
                        dest="shape_path")

    parser.add_argument("-dpfad", action="store",
                        help="Dateipfad für Ergebnisdownload, Dateiendung bestimmt Datentyp: shp/csv/xls (Pflicht bei Download)",
                        dest="download_file")

    parser.add_argument("-jahr", action="store",
                        help="Jahr der herunterzuladenden Ergebnisse",
                        dest="year")

    parser.add_argument("-schema", action="store",
                        help="Datenbankschema (Pflicht bei Shapefile-Upload und Verschneidung)",
                        dest="schema")

    parser.add_argument("-name", action="store",
                        help="Name der Tabelle mit den Shapes (optional bei Shapefile-Upload, Pflicht bei Verschneidung)",
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

    #parser.add_argument("-run", action="store",
                        #help="angegebenes Szenario ausführen",
                        #dest="scenario_name", default=None)

    arguments = parser.parse_args()

    if arguments.upload and (not arguments.shape_path or not arguments.schema):
        print('Um ein Shapefile hochzuladen, müssen Pfad zum Shapefile und Zielschema angegeben sein.')
        exit(1)

    if arguments.intersection and (not arguments.table_name or not arguments.schema):
        print('Um eine Verschneidung durchzuführen hochzuladen, müssen Schema und Tabellenname mit den Shapes angegeben sein.')
        exit(1)

    if arguments.download and (not arguments.table_name or not arguments.schema or not arguments.download_file or not arguments.year):
        print('Für den Download von Ergebnissen, müssen Schema und Tabellenname der Aggregationsstufe, ein Dateiname und das Jahr der Ergebnisse angegeben werden.')
        exit(1)

    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.exec_arguments(arguments)
    sys.exit(app.exec_())

if __name__ == "__main__":
    startmain()
