# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from verschneidungstool.control import MainWindow
import sys
import os
from PyQt5 import QtGui, QtWidgets, QtCore
from verschneidungstool.config import Config, DEFAULT_SRID

config = Config()
config.read()

def startmain():

    parser = ArgumentParser(description="GUI Verschneidungstool")

    parser.add_argument("--config", action="store",
                        help="Pfad zu einer XML-Config-Datei mit den Verbindungsdaten und Pfaden zu den Postgres-Tools (optional)",
                        dest="config")

    parser.add_argument("--upload", action="store_true",
                        help="Shapefile hochladen",
                        dest="upload")

    parser.add_argument("--verschneiden", action="store_true",
                        help="Verschneidung durchführen",
                        dest="intersection")

    parser.add_argument("--download", action="store_true",
                        help="Ergebnisse herunterladen",
                        dest="download")

    parser.add_argument("--shapefile", action="store",
                        help="Pfad zur Datei (Pflicht bei Shapefile-Upload)",
                        dest="shape_path")

    parser.add_argument("--dpfad", action="store",
                        help="Dateipfad für Ergebnisdownload, Dateiendung bestimmt Datentyp: shp/csv/xls (Pflicht bei Download)",
                        dest="download_file")

    parser.add_argument('-j', "--jahr", action="store", type=int,
                        help="Jahr der herunterzuladenden Ergebnisse",
                        dest="year")

    parser.add_argument("--schema", action="store", default='verkehrszellen',
                        help="Datenbankschema (Pflicht bei Shapefile-Upload und Verschneidung)",
                        dest="schema")

    parser.add_argument("--name", action="store",
                        help="Name der Tabelle mit den Shapes (optional bei Shapefile-Upload, Pflicht bei Verschneidung)",
                        dest="table_name")

    parser.add_argument("--srid", action="store", default=DEFAULT_SRID,
                        type=int,
                        help="Projektion des Shapefiles bei Shapefile-Upload (default: {d})".format(d=DEFAULT_SRID),
                        dest="srid")

    DEFAULT_ColId = 'no'
    parser.add_argument("--gebiet_id", action="store", default=DEFAULT_ColId,
                        help="Spalte für ID bei Shapefile-Upload (Default: {d})".format(d=DEFAULT_ColId),
                        dest="c_id")

    DEFAULT_ColName = 'name'
    parser.add_argument("--gebiet_name", action="store", default=DEFAULT_ColName,
                        help="Spalte mit Gebietsnamen bei Shapefile-Upload (Default: {d})".format(d=DEFAULT_ColName),
                        dest="c_name")

    arguments = parser.parse_args()

    if arguments.download_file:
        ext = os.path.splitext(arguments.download_file)
        if not ext[1] in ['.csv', '.shp', '.xls']:
            print('gültige Dateiendung für Datentyp .shp, .csv oder .xls wählen')
            exit(1)

    if arguments.upload and (not arguments.shape_path or not arguments.schema):
        print('Um ein Shapefile hochzuladen, müssen Pfad zum Shapefile und Zielschema angegeben sein.')
        exit(1)

    if arguments.intersection and (not arguments.table_name or not arguments.schema):
        print('Um eine Verschneidung durchzuführen hochzuladen, müssen Schema und Tabellenname mit den Shapes angegeben sein.')
        exit(1)

    if arguments.download and (not arguments.table_name or not arguments.schema or not arguments.download_file or not arguments.year):
        print('Für den Download von Ergebnissen, müssen Schema und Tabellenname der Aggregationsstufe, ein Dateiname und das Jahr der Ergebnisse angegeben werden.')
        exit(1)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    mainwindow = MainWindow()
    mainwindow.show()
    mainwindow.exec_arguments(arguments)
    sys.exit(app.exec_())

if __name__ == "__main__":
    startmain()
