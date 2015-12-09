# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName(_fromUtf8("ProgressDialog"))
        ProgressDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ProgressDialog.resize(635, 347)
        ProgressDialog.setMinimumSize(QtCore.QSize(410, 210))
        ProgressDialog.setMaximumSize(QtCore.QSize(10000, 10000))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ProgressDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.log_edit = QtGui.QTextEdit(ProgressDialog)
        self.log_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.log_edit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.log_edit.setReadOnly(True)
        self.log_edit.setObjectName(_fromUtf8("log_edit"))
        self.verticalLayout_2.addWidget(self.log_edit)
        self.progress_bar = QtGui.QProgressBar(ProgressDialog)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.startButton = QtGui.QPushButton(ProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setMinimumSize(QtCore.QSize(87, 23))
        self.startButton.setMaximumSize(QtCore.QSize(87, 23))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.cancelButton = QtGui.QPushButton(ProgressDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(87, 23))
        self.cancelButton.setMaximumSize(QtCore.QSize(87, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Fortschritt", None))
        self.startButton.setText(_translate("ProgressDialog", "Start", None))
        self.cancelButton.setText(_translate("ProgressDialog", "Abbrechen", None))

