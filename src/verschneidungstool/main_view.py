# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 498)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.db_frame = QtWidgets.QFrame(self.centralwidget)
        self.db_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.db_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.db_frame.setObjectName("db_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.db_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dbconnect_button = QtWidgets.QPushButton(self.db_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbconnect_button.sizePolicy().hasHeightForWidth())
        self.dbconnect_button.setSizePolicy(sizePolicy)
        self.dbconnect_button.setObjectName("dbconnect_button")
        self.verticalLayout_2.addWidget(self.dbconnect_button)
        self.gridLayout_4.addWidget(self.db_frame, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 2, 0, 1, 1)
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setEnabled(False)
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.main_frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.main_frame)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.stations_combo = QtWidgets.QComboBox(self.groupBox_3)
        self.stations_combo.setMinimumSize(QtCore.QSize(150, 0))
        self.stations_combo.setObjectName("stations_combo")
        self.verticalLayout_6.addWidget(self.stations_combo)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.delete_stations_button = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_stations_button.sizePolicy().hasHeightForWidth())
        self.delete_stations_button.setSizePolicy(sizePolicy)
        self.delete_stations_button.setObjectName("delete_stations_button")
        self.horizontalLayout_2.addWidget(self.delete_stations_button)
        self.add_stations_button = QtWidgets.QPushButton(self.groupBox_3)
        self.add_stations_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.add_stations_button.setObjectName("add_stations_button")
        self.horizontalLayout_2.addWidget(self.add_stations_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.layer_combo = QtWidgets.QComboBox(self.groupBox)
        self.layer_combo.setMinimumSize(QtCore.QSize(150, 0))
        self.layer_combo.setObjectName("layer_combo")
        self.verticalLayout_5.addWidget(self.layer_combo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delete_layer_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_layer_button.sizePolicy().hasHeightForWidth())
        self.delete_layer_button.setSizePolicy(sizePolicy)
        self.delete_layer_button.setObjectName("delete_layer_button")
        self.horizontalLayout.addWidget(self.delete_layer_button)
        self.add_layer_button = QtWidgets.QPushButton(self.groupBox)
        self.add_layer_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.add_layer_button.setObjectName("add_layer_button")
        self.horizontalLayout.addWidget(self.add_layer_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.intersect_frame = QtWidgets.QGroupBox(self.main_frame)
        self.intersect_frame.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intersect_frame.sizePolicy().hasHeightForWidth())
        self.intersect_frame.setSizePolicy(sizePolicy)
        self.intersect_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.intersect_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.intersect_frame.setObjectName("intersect_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.intersect_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.intersect_button = QtWidgets.QPushButton(self.intersect_frame)
        self.intersect_button.setEnabled(False)
        self.intersect_button.setObjectName("intersect_button")
        self.verticalLayout_3.addWidget(self.intersect_button)
        self.horizontalLayout_4.addWidget(self.intersect_frame)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(self.main_frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_9.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.main_frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.year_combo = QtWidgets.QComboBox(self.groupBox_2)
        self.year_combo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.year_combo.setObjectName("year_combo")
        self.verticalLayout.addWidget(self.year_combo)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.download_frame = QtWidgets.QGroupBox(self.main_frame)
        self.download_frame.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.download_frame.sizePolicy().hasHeightForWidth())
        self.download_frame.setSizePolicy(sizePolicy)
        self.download_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.download_frame.setObjectName("download_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.download_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.shape_radio_button = QtWidgets.QRadioButton(self.download_frame)
        self.shape_radio_button.setChecked(True)
        self.shape_radio_button.setObjectName("shape_radio_button")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.shape_radio_button)
        self.verticalLayout_4.addWidget(self.shape_radio_button)
        self.csv_radio_button = QtWidgets.QRadioButton(self.download_frame)
        self.csv_radio_button.setObjectName("csv_radio_button")
        self.buttonGroup.addButton(self.csv_radio_button)
        self.verticalLayout_4.addWidget(self.csv_radio_button)
        self.excel_radio_button = QtWidgets.QRadioButton(self.download_frame)
        self.excel_radio_button.setObjectName("excel_radio_button")
        self.buttonGroup.addButton(self.excel_radio_button)
        self.verticalLayout_4.addWidget(self.excel_radio_button)
        self.visum_radio_button = QtWidgets.QRadioButton(self.download_frame)
        self.visum_radio_button.setEnabled(False)
        self.visum_radio_button.setObjectName("visum_radio_button")
        self.verticalLayout_4.addWidget(self.visum_radio_button)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.download_frame)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.visum_mod_input = QtWidgets.QSpinBox(self.download_frame)
        self.visum_mod_input.setEnabled(False)
        self.visum_mod_input.setMinimum(1)
        self.visum_mod_input.setMaximum(9999)
        self.visum_mod_input.setProperty("value", 99)
        self.visum_mod_input.setObjectName("visum_mod_input")
        self.horizontalLayout_3.addWidget(self.visum_mod_input)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.results_button = QtWidgets.QPushButton(self.download_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.results_button.sizePolicy().hasHeightForWidth())
        self.results_button.setSizePolicy(sizePolicy)
        self.results_button.setObjectName("results_button")
        self.verticalLayout_4.addWidget(self.results_button)
        self.verticalLayout_7.addWidget(self.download_frame)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.structure_tree = QtWidgets.QTreeWidget(self.main_frame)
        self.structure_tree.setColumnCount(2)
        self.structure_tree.setObjectName("structure_tree")
        self.structure_tree.headerItem().setText(0, "1")
        self.structure_tree.headerItem().setText(1, "2")
        self.horizontalLayout_5.addWidget(self.structure_tree)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.line_3 = QtWidgets.QFrame(self.main_frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_9.addWidget(self.line_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.download_tables_frame = QtWidgets.QGroupBox(self.main_frame)
        self.download_tables_frame.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.download_tables_frame.sizePolicy().hasHeightForWidth())
        self.download_tables_frame.setSizePolicy(sizePolicy)
        self.download_tables_frame.setMaximumSize(QtCore.QSize(300, 150))
        self.download_tables_frame.setObjectName("download_tables_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.download_tables_frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.download_tables_button = QtWidgets.QPushButton(self.download_tables_frame)
        self.download_tables_button.setEnabled(False)
        self.download_tables_button.setObjectName("download_tables_button")
        self.verticalLayout_8.addWidget(self.download_tables_button)
        self.horizontalLayout_6.addWidget(self.download_tables_frame)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.gridLayout_4.addWidget(self.main_frame, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 776, 18))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtWidgets.QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEinstellungen = QtWidgets.QAction(MainWindow)
        self.actionEinstellungen.setObjectName("actionEinstellungen")
        self.actionBeenden = QtWidgets.QAction(MainWindow)
        self.actionBeenden.setObjectName("actionBeenden")
        self.menuDatei.addAction(self.actionEinstellungen)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBeenden)
        self.menubar.addAction(self.menuDatei.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Verschneidungstool"))
        self.dbconnect_button.setText(_translate("MainWindow", "mit Datenbank verbinden"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Bahnhaltestellen"))
        self.delete_stations_button.setText(_translate("MainWindow", "Löschen"))
        self.add_stations_button.setText(_translate("MainWindow", "Neuer Layer"))
        self.groupBox.setTitle(_translate("MainWindow", "Aggregationsstufe"))
        self.delete_layer_button.setText(_translate("MainWindow", "Löschen"))
        self.add_layer_button.setText(_translate("MainWindow", "Neuer Layer"))
        self.intersect_frame.setTitle(_translate("MainWindow", "Verschneiden"))
        self.intersect_button.setText(_translate("MainWindow", "Verschneidung berechnen"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Jahr"))
        self.download_frame.setTitle(_translate("MainWindow", "Ergebnisse"))
        self.shape_radio_button.setText(_translate("MainWindow", "als Shapefile"))
        self.csv_radio_button.setText(_translate("MainWindow", "als csv-Datei"))
        self.excel_radio_button.setText(_translate("MainWindow", "als Exceltabelle"))
        self.visum_radio_button.setText(_translate("MainWindow", "als Visumtransferdatei"))
        self.label.setText(_translate("MainWindow", "Mod-nr."))
        self.results_button.setText(_translate("MainWindow", "Herunterladen"))
        self.download_tables_frame.setTitle(_translate("MainWindow", "einzelne Strukturdaten"))
        self.download_tables_button.setText(_translate("MainWindow", "Herunterladen"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.actionEinstellungen.setText(_translate("MainWindow", "Einstellungen"))
        self.actionBeenden.setText(_translate("MainWindow", "Beenden"))

import gui_rc
