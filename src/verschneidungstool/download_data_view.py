# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_data.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DownloadDataDialog(object):
    def setupUi(self, DownloadDataDialog):
        DownloadDataDialog.setObjectName("DownloadDataDialog")
        DownloadDataDialog.resize(470, 394)
        self.gridLayout = QtWidgets.QGridLayout(DownloadDataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.dir_edit = QtWidgets.QLineEdit(DownloadDataDialog)
        self.dir_edit.setMinimumSize(QtCore.QSize(200, 0))
        self.dir_edit.setObjectName("dir_edit")
        self.gridLayout.addWidget(self.dir_edit, 1, 2, 1, 3)
        self.cancel_button = QtWidgets.QPushButton(DownloadDataDialog)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 3, 5, 1, 1)
        self.tables_to_download_tree = QtWidgets.QTreeWidget(DownloadDataDialog)
        self.tables_to_download_tree.setColumnCount(2)
        self.tables_to_download_tree.setObjectName("tables_to_download_tree")
        self.tables_to_download_tree.headerItem().setText(0, "1")
        self.tables_to_download_tree.headerItem().setText(1, "2")
        self.tables_to_download_tree.header().setVisible(True)
        self.gridLayout.addWidget(self.tables_to_download_tree, 0, 1, 1, 5)
        self.download_button = QtWidgets.QPushButton(DownloadDataDialog)
        self.download_button.setObjectName("download_button")
        self.gridLayout.addWidget(self.download_button, 3, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 3)
        self.select_dir_button = QtWidgets.QPushButton(DownloadDataDialog)
        self.select_dir_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.select_dir_button.setObjectName("select_dir_button")
        self.gridLayout.addWidget(self.select_dir_button, 1, 5, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(DownloadDataDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)

        self.retranslateUi(DownloadDataDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDataDialog)

    def retranslateUi(self, DownloadDataDialog):
        _translate = QtCore.QCoreApplication.translate
        DownloadDataDialog.setWindowTitle(_translate("DownloadDataDialog", "Strukturdaten herunterladen"))
        self.cancel_button.setText(_translate("DownloadDataDialog", "Abbrechen"))
        self.download_button.setText(_translate("DownloadDataDialog", "Herunterladen"))
        self.select_dir_button.setText(_translate("DownloadDataDialog", "..."))
        self.label.setText(_translate("DownloadDataDialog", "Zielordner"))

