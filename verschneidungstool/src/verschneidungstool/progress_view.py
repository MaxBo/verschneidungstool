# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        application_modal = getattr(QtCore.Qt, "ApplicationModal", None)
        if application_modal is None:
            application_modal = QtCore.Qt.WindowModality.ApplicationModal
        ProgressDialog.setWindowModality(application_modal)
        ProgressDialog.resize(635, 347)
        ProgressDialog.setMinimumSize(QtCore.QSize(410, 210))
        ProgressDialog.setMaximumSize(QtCore.QSize(10000, 10000))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ProgressDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.log_edit = QtWidgets.QTextEdit(ProgressDialog)
        scroll_always_on = getattr(QtCore.Qt, "ScrollBarAlwaysOn", None)
        if scroll_always_on is None:
            scroll_always_on = QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        self.log_edit.setHorizontalScrollBarPolicy(scroll_always_on)
        no_wrap = getattr(QtWidgets.QTextEdit, "NoWrap", None)
        if no_wrap is None:
            no_wrap = QtWidgets.QTextEdit.LineWrapMode.NoWrap
        self.log_edit.setLineWrapMode(no_wrap)
        self.log_edit.setReadOnly(True)
        self.log_edit.setObjectName("log_edit")
        self.verticalLayout_2.addWidget(self.log_edit)
        self.progress_bar = QtWidgets.QProgressBar(ProgressDialog)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.startButton = QtWidgets.QPushButton(ProgressDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setMinimumSize(QtCore.QSize(87, 23))
        self.startButton.setMaximumSize(QtCore.QSize(87, 23))
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.cancelButton = QtWidgets.QPushButton(ProgressDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(87, 23))
        self.cancelButton.setMaximumSize(QtCore.QSize(87, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Fortschritt"))
        self.startButton.setText(_translate("ProgressDialog", "Start"))
        self.cancelButton.setText(_translate("ProgressDialog", "Abbrechen"))

