# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Dec 16 11:33:04 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(724, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/favicon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.db_frame = QtGui.QFrame(self.centralwidget)
        self.db_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.db_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.db_frame.setObjectName(_fromUtf8("db_frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.db_frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.dbconnect_button = QtGui.QPushButton(self.db_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbconnect_button.sizePolicy().hasHeightForWidth())
        self.dbconnect_button.setSizePolicy(sizePolicy)
        self.dbconnect_button.setObjectName(_fromUtf8("dbconnect_button"))
        self.verticalLayout_2.addWidget(self.dbconnect_button)
        self.gridLayout_4.addWidget(self.db_frame, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_4.addWidget(self.line_2, 2, 0, 1, 1)
        self.main_frame = QtGui.QFrame(self.centralwidget)
        self.main_frame.setEnabled(False)
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName(_fromUtf8("main_frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.main_frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.line = QtGui.QFrame(self.main_frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 6, 1, 1, 4)
        self.download_frame = QtGui.QGroupBox(self.main_frame)
        self.download_frame.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.download_frame.sizePolicy().hasHeightForWidth())
        self.download_frame.setSizePolicy(sizePolicy)
        self.download_frame.setMaximumSize(QtCore.QSize(300, 150))
        self.download_frame.setObjectName(_fromUtf8("download_frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.download_frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.shape_radio_button = QtGui.QRadioButton(self.download_frame)
        self.shape_radio_button.setChecked(True)
        self.shape_radio_button.setObjectName(_fromUtf8("shape_radio_button"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.shape_radio_button)
        self.verticalLayout_4.addWidget(self.shape_radio_button)
        self.csv_radio_button = QtGui.QRadioButton(self.download_frame)
        self.csv_radio_button.setObjectName(_fromUtf8("csv_radio_button"))
        self.buttonGroup.addButton(self.csv_radio_button)
        self.verticalLayout_4.addWidget(self.csv_radio_button)
        self.excel_radio_button = QtGui.QRadioButton(self.download_frame)
        self.excel_radio_button.setObjectName(_fromUtf8("excel_radio_button"))
        self.buttonGroup.addButton(self.excel_radio_button)
        self.verticalLayout_4.addWidget(self.excel_radio_button)
        self.radioButton_4 = QtGui.QRadioButton(self.download_frame)
        self.radioButton_4.setEnabled(False)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.verticalLayout_4.addWidget(self.radioButton_4)
        self.results_button = QtGui.QPushButton(self.download_frame)
        self.results_button.setObjectName(_fromUtf8("results_button"))
        self.verticalLayout_4.addWidget(self.results_button)
        self.gridLayout_2.addWidget(self.download_frame, 9, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.main_frame)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.stations_combo = QtGui.QComboBox(self.groupBox_3)
        self.stations_combo.setMinimumSize(QtCore.QSize(150, 0))
        self.stations_combo.setObjectName(_fromUtf8("stations_combo"))
        self.verticalLayout_6.addWidget(self.stations_combo)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.delete_stations_button = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_stations_button.sizePolicy().hasHeightForWidth())
        self.delete_stations_button.setSizePolicy(sizePolicy)
        self.delete_stations_button.setObjectName(_fromUtf8("delete_stations_button"))
        self.horizontalLayout_2.addWidget(self.delete_stations_button)
        self.add_stations_button = QtGui.QPushButton(self.groupBox_3)
        self.add_stations_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.add_stations_button.setObjectName(_fromUtf8("add_stations_button"))
        self.horizontalLayout_2.addWidget(self.add_stations_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 2, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.main_frame)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.year_combo = QtGui.QComboBox(self.groupBox_2)
        self.year_combo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.year_combo.setObjectName(_fromUtf8("year_combo"))
        self.verticalLayout.addWidget(self.year_combo)
        self.gridLayout_2.addWidget(self.groupBox_2, 8, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.layer_combo = QtGui.QComboBox(self.groupBox)
        self.layer_combo.setMinimumSize(QtCore.QSize(150, 0))
        self.layer_combo.setObjectName(_fromUtf8("layer_combo"))
        self.verticalLayout_5.addWidget(self.layer_combo)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.delete_layer_button = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_layer_button.sizePolicy().hasHeightForWidth())
        self.delete_layer_button.setSizePolicy(sizePolicy)
        self.delete_layer_button.setObjectName(_fromUtf8("delete_layer_button"))
        self.horizontalLayout.addWidget(self.delete_layer_button)
        self.add_layer_button = QtGui.QPushButton(self.groupBox)
        self.add_layer_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.add_layer_button.setObjectName(_fromUtf8("add_layer_button"))
        self.horizontalLayout.addWidget(self.add_layer_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)
        self.intersect_frame = QtGui.QGroupBox(self.main_frame)
        self.intersect_frame.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intersect_frame.sizePolicy().hasHeightForWidth())
        self.intersect_frame.setSizePolicy(sizePolicy)
        self.intersect_frame.setMinimumSize(QtCore.QSize(0, 60))
        self.intersect_frame.setMaximumSize(QtCore.QSize(300, 60))
        self.intersect_frame.setObjectName(_fromUtf8("intersect_frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.intersect_frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.intersect_button = QtGui.QPushButton(self.intersect_frame)
        self.intersect_button.setEnabled(False)
        self.intersect_button.setObjectName(_fromUtf8("intersect_button"))
        self.verticalLayout_3.addWidget(self.intersect_button)
        self.gridLayout_2.addWidget(self.intersect_frame, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 10, 1, 1, 1)
        self.structure_tree = QtGui.QTreeWidget(self.main_frame)
        self.structure_tree.setColumnCount(2)
        self.structure_tree.setObjectName(_fromUtf8("structure_tree"))
        self.structure_tree.headerItem().setText(0, _fromUtf8("1"))
        self.structure_tree.headerItem().setText(1, _fromUtf8("2"))
        self.gridLayout_2.addWidget(self.structure_tree, 7, 2, 6, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 7, 1, 1, 1)
        self.download_tables_frame = QtGui.QGroupBox(self.main_frame)
        self.download_tables_frame.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.download_tables_frame.sizePolicy().hasHeightForWidth())
        self.download_tables_frame.setSizePolicy(sizePolicy)
        self.download_tables_frame.setMaximumSize(QtCore.QSize(300, 150))
        self.download_tables_frame.setObjectName(_fromUtf8("download_tables_frame"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.download_tables_frame)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.download_tables_button = QtGui.QPushButton(self.download_tables_frame)
        self.download_tables_button.setEnabled(False)
        self.download_tables_button.setObjectName(_fromUtf8("download_tables_button"))
        self.verticalLayout_8.addWidget(self.download_tables_button)
        self.gridLayout_2.addWidget(self.download_tables_frame, 14, 1, 1, 1)
        self.line_3 = QtGui.QFrame(self.main_frame)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 13, 1, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 4, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 14, 2, 1, 3)
        self.gridLayout_4.addWidget(self.main_frame, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDatei = QtGui.QMenu(self.menubar)
        self.menuDatei.setObjectName(_fromUtf8("menuDatei"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionEinstellungen = QtGui.QAction(MainWindow)
        self.actionEinstellungen.setObjectName(_fromUtf8("actionEinstellungen"))
        self.actionBeenden = QtGui.QAction(MainWindow)
        self.actionBeenden.setObjectName(_fromUtf8("actionBeenden"))
        self.menuDatei.addAction(self.actionEinstellungen)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBeenden)
        self.menubar.addAction(self.menuDatei.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Verschneidungstool", None))
        self.dbconnect_button.setText(_translate("MainWindow", "mit Datenbank verbinden", None))
        self.download_frame.setTitle(_translate("MainWindow", "Ergebnisse", None))
        self.shape_radio_button.setText(_translate("MainWindow", "als Shapefile", None))
        self.csv_radio_button.setText(_translate("MainWindow", "als csv-Datei", None))
        self.excel_radio_button.setText(_translate("MainWindow", "als Exceltabelle", None))
        self.radioButton_4.setText(_translate("MainWindow", "als FileGeoDatabase", None))
        self.results_button.setText(_translate("MainWindow", "Herunterladen", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Bahnhaltestellen", None))
        self.delete_stations_button.setText(_translate("MainWindow", "Löschen", None))
        self.add_stations_button.setText(_translate("MainWindow", "Neuer Layer", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Jahr", None))
        self.groupBox.setTitle(_translate("MainWindow", "Aggregationsstufe", None))
        self.delete_layer_button.setText(_translate("MainWindow", "Löschen", None))
        self.add_layer_button.setText(_translate("MainWindow", "Neuer Layer", None))
        self.intersect_frame.setTitle(_translate("MainWindow", "Verschneiden", None))
        self.intersect_button.setText(_translate("MainWindow", "Verschneidung berechnen", None))
        self.download_tables_frame.setTitle(_translate("MainWindow", "einzelne Strukturdaten", None))
        self.download_tables_button.setText(_translate("MainWindow", "Herunterladen", None))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
        self.actionEinstellungen.setText(_translate("MainWindow", "Einstellungen", None))
        self.actionBeenden.setText(_translate("MainWindow", "Beenden", None))

import gui_rc
