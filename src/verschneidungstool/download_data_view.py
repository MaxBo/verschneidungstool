# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_data.ui'
#
# Created: Wed Dec 16 09:49:13 2015
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

class Ui_DownloadDataDialog(object):
    def setupUi(self, DownloadDataDialog):
        DownloadDataDialog.setObjectName(_fromUtf8("DownloadDataDialog"))
        DownloadDataDialog.resize(470, 394)
        self.gridLayout = QtGui.QGridLayout(DownloadDataDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dir_edit = QtGui.QLineEdit(DownloadDataDialog)
        self.dir_edit.setMinimumSize(QtCore.QSize(200, 0))
        self.dir_edit.setObjectName(_fromUtf8("dir_edit"))
        self.gridLayout.addWidget(self.dir_edit, 1, 2, 1, 3)
        self.cancel_button = QtGui.QPushButton(DownloadDataDialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.gridLayout.addWidget(self.cancel_button, 3, 5, 1, 1)
        self.tables_to_download_tree = QtGui.QTreeWidget(DownloadDataDialog)
        self.tables_to_download_tree.setColumnCount(2)
        self.tables_to_download_tree.setObjectName(_fromUtf8("tables_to_download_tree"))
        self.tables_to_download_tree.headerItem().setText(0, _fromUtf8("1"))
        self.tables_to_download_tree.headerItem().setText(1, _fromUtf8("2"))
        self.tables_to_download_tree.header().setVisible(True)
        self.gridLayout.addWidget(self.tables_to_download_tree, 0, 1, 1, 5)
        self.download_button = QtGui.QPushButton(DownloadDataDialog)
        self.download_button.setObjectName(_fromUtf8("download_button"))
        self.gridLayout.addWidget(self.download_button, 3, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 3)
        self.select_dir_button = QtGui.QPushButton(DownloadDataDialog)
        self.select_dir_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.select_dir_button.setObjectName(_fromUtf8("select_dir_button"))
        self.gridLayout.addWidget(self.select_dir_button, 1, 5, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtGui.QLabel(DownloadDataDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)

        self.retranslateUi(DownloadDataDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDataDialog)

    def retranslateUi(self, DownloadDataDialog):
        DownloadDataDialog.setWindowTitle(_translate("DownloadDataDialog", "Einzeldaten herunterladen", None))
        self.cancel_button.setText(_translate("DownloadDataDialog", "Abbrechen", None))
        self.download_button.setText(_translate("DownloadDataDialog", "Herunterladen", None))
        self.select_dir_button.setText(_translate("DownloadDataDialog", "...", None))
        self.label.setText(_translate("DownloadDataDialog", "Zielordner", None))

