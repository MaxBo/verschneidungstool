# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Wed Mar 16 11:14:37 2016
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(550, 263)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QtCore.QSize(550, 250))
        Settings.setMaximumSize(QtCore.QSize(550, 300))
        Settings.setSizeGripEnabled(False)
        Settings.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.load_config_button = QtGui.QPushButton(Settings)
        self.load_config_button.setObjectName(_fromUtf8("load_config_button"))
        self.horizontalLayout.addWidget(self.load_config_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.OK_button = QtGui.QPushButton(Settings)
        self.OK_button.setObjectName(_fromUtf8("OK_button"))
        self.horizontalLayout.addWidget(self.OK_button)
        self.cancel_button = QtGui.QPushButton(Settings)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout.addWidget(self.cancel_button)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Settings)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.dblogin_tab = QtGui.QWidget()
        self.dblogin_tab.setObjectName(_fromUtf8("dblogin_tab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.dblogin_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 491, 161))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.username_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.username_edit.setObjectName(_fromUtf8("username_edit"))
        self.gridLayout_3.addWidget(self.username_edit, 0, 2, 1, 4)
        self.password_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.password_edit.setObjectName(_fromUtf8("password_edit"))
        self.gridLayout_3.addWidget(self.password_edit, 1, 2, 1, 4)
        self.srid_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.srid_edit.setObjectName(_fromUtf8("srid_edit"))
        self.gridLayout_3.addWidget(self.srid_edit, 6, 2, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 6, 0, 1, 1)
        self.srid_default_button = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.srid_default_button.setObjectName(_fromUtf8("srid_default_button"))
        self.gridLayout_3.addWidget(self.srid_default_button, 6, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 5, 0, 1, 1)
        self.port_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.port_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.port_edit.setObjectName(_fromUtf8("port_edit"))
        self.gridLayout_3.addWidget(self.port_edit, 3, 5, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem2, 2, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 3, 4, 1, 1)
        self.host_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.host_edit.setObjectName(_fromUtf8("host_edit"))
        self.gridLayout_3.addWidget(self.host_edit, 3, 2, 1, 2)
        self.dbname_edit = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.dbname_edit.setObjectName(_fromUtf8("dbname_edit"))
        self.gridLayout_3.addWidget(self.dbname_edit, 4, 2, 1, 2)
        self.tabWidget.addTab(self.dblogin_tab, _fromUtf8(""))
        self.env_tab = QtGui.QWidget()
        self.env_tab.setObjectName(_fromUtf8("env_tab"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.env_tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 30, 491, 128))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)
        self.psql_browse_button = QtGui.QPushButton(self.gridLayoutWidget_3)
        self.psql_browse_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.psql_browse_button.setObjectName(_fromUtf8("psql_browse_button"))
        self.gridLayout_4.addWidget(self.psql_browse_button, 0, 3, 1, 1)
        self.shp2pgsql_browse_button = QtGui.QPushButton(self.gridLayoutWidget_3)
        self.shp2pgsql_browse_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.shp2pgsql_browse_button.setObjectName(_fromUtf8("shp2pgsql_browse_button"))
        self.gridLayout_4.addWidget(self.shp2pgsql_browse_button, 1, 3, 1, 1)
        self.shp2pgsql_edit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.shp2pgsql_edit.setObjectName(_fromUtf8("shp2pgsql_edit"))
        self.gridLayout_4.addWidget(self.shp2pgsql_edit, 1, 1, 1, 1)
        self.psql_edit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.psql_edit.setObjectName(_fromUtf8("psql_edit"))
        self.gridLayout_4.addWidget(self.psql_edit, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 3, 0, 1, 1)
        self.pgsql2shp_edit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.pgsql2shp_edit.setObjectName(_fromUtf8("pgsql2shp_edit"))
        self.gridLayout_4.addWidget(self.pgsql2shp_edit, 3, 1, 1, 1)
        self.pgsql2shp_browse_button = QtGui.QPushButton(self.gridLayoutWidget_3)
        self.pgsql2shp_browse_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pgsql2shp_browse_button.setObjectName(_fromUtf8("pgsql2shp_browse_button"))
        self.gridLayout_4.addWidget(self.pgsql2shp_browse_button, 3, 3, 1, 1)
        self.tabWidget.addTab(self.env_tab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Einstellungen", None))
        self.load_config_button.setText(_translate("Settings", "Konfiguration laden", None))
        self.OK_button.setText(_translate("Settings", "OK", None))
        self.cancel_button.setText(_translate("Settings", "Abbrechen", None))
        self.label_5.setText(_translate("Settings", "Passwort", None))
        self.label.setText(_translate("Settings", "DB-Projektion (SRID)", None))
        self.srid_default_button.setText(_translate("Settings", "Default", None))
        self.label_8.setText(_translate("Settings", "Datenbankname", None))
        self.label_3.setText(_translate("Settings", "Username", None))
        self.label_7.setText(_translate("Settings", "Host", None))
        self.label_9.setText(_translate("Settings", "Port", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dblogin_tab), _translate("Settings", "Datenbankverbindung", None))
        self.label_6.setText(_translate("Settings", "psql.exe", None))
        self.label_10.setText(_translate("Settings", "shp2pgsql.exe", None))
        self.psql_browse_button.setText(_translate("Settings", "...", None))
        self.shp2pgsql_browse_button.setText(_translate("Settings", "...", None))
        self.label_11.setText(_translate("Settings", "pgsql2shp.exe", None))
        self.pgsql2shp_browse_button.setText(_translate("Settings", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.env_tab), _translate("Settings", "Pfade", None))

