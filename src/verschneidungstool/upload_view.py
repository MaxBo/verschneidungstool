# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload.ui'
#
# Created: Fri Nov 27 10:47:39 2015
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

class Ui_Upload(object):
    def setupUi(self, Upload):
        Upload.setObjectName(_fromUtf8("Upload"))
        Upload.resize(550, 420)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Upload.sizePolicy().hasHeightForWidth())
        Upload.setSizePolicy(sizePolicy)
        Upload.setMinimumSize(QtCore.QSize(550, 420))
        Upload.setMaximumSize(QtCore.QSize(550, 420))
        Upload.setSizeGripEnabled(False)
        Upload.setModal(True)
        self.layoutWidget_2 = QtGui.QWidget(Upload)
        self.layoutWidget_2.setGeometry(QtCore.QRect(0, 370, 541, 41))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.OK_button = QtGui.QPushButton(self.layoutWidget_2)
        self.OK_button.setObjectName(_fromUtf8("OK_button"))
        self.horizontalLayout_2.addWidget(self.OK_button)
        self.cancel_button = QtGui.QPushButton(self.layoutWidget_2)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.upload_frame = QtGui.QGroupBox(Upload)
        self.upload_frame.setGeometry(QtCore.QRect(0, 0, 561, 271))
        self.upload_frame.setObjectName(_fromUtf8("upload_frame"))
        self.gridLayoutWidget = QtGui.QWidget(self.upload_frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 531, 241))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.upload_layout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.upload_layout.setMargin(0)
        self.upload_layout.setObjectName(_fromUtf8("upload_layout"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.shapefile_edit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.shapefile_edit.setObjectName(_fromUtf8("shapefile_edit"))
        self.gridLayout_4.addWidget(self.shapefile_edit, 0, 1, 1, 1)
        self.schema_combo = QtGui.QComboBox(self.gridLayoutWidget)
        self.schema_combo.setObjectName(_fromUtf8("schema_combo"))
        self.gridLayout_4.addWidget(self.schema_combo, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)
        self.shapefile_browse_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.shapefile_browse_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.shapefile_browse_button.setObjectName(_fromUtf8("shapefile_browse_button"))
        self.gridLayout_4.addWidget(self.shapefile_browse_button, 0, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.name_edit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.name_edit.setObjectName(_fromUtf8("name_edit"))
        self.gridLayout_4.addWidget(self.name_edit, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)
        self.projection_combo = QtGui.QComboBox(self.gridLayoutWidget)
        self.projection_combo.setEditable(False)
        self.projection_combo.setObjectName(_fromUtf8("projection_combo"))
        self.gridLayout_4.addWidget(self.projection_combo, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 3, 1, 1, 1)
        self.check_projection_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.check_projection_button.setObjectName(_fromUtf8("check_projection_button"))
        self.gridLayout_4.addWidget(self.check_projection_button, 4, 2, 1, 1)
        self.upload_layout.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.upload_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.upload_button.setObjectName(_fromUtf8("upload_button"))
        self.horizontalLayout.addWidget(self.upload_button)
        self.upload_layout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.message_edit = QtGui.QTextEdit(self.gridLayoutWidget)
        self.message_edit.setEnabled(True)
        self.message_edit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.message_edit.setReadOnly(True)
        self.message_edit.setObjectName(_fromUtf8("message_edit"))
        self.upload_layout.addWidget(self.message_edit, 2, 0, 1, 1)
        self.identifiers_frame = QtGui.QGroupBox(Upload)
        self.identifiers_frame.setGeometry(QtCore.QRect(0, 280, 561, 91))
        self.identifiers_frame.setObjectName(_fromUtf8("identifiers_frame"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.identifiers_frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 531, 61))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.select_ids_layout = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.select_ids_layout.setMargin(0)
        self.select_ids_layout.setObjectName(_fromUtf8("select_ids_layout"))
        self.names_combo = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.names_combo.setObjectName(_fromUtf8("names_combo"))
        self.select_ids_layout.addWidget(self.names_combo, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.select_ids_layout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.select_ids_layout.addWidget(self.label_4, 0, 0, 1, 1)
        self.pkey_combo = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.pkey_combo.setObjectName(_fromUtf8("pkey_combo"))
        self.select_ids_layout.addWidget(self.pkey_combo, 0, 1, 1, 1)

        self.retranslateUi(Upload)
        QtCore.QMetaObject.connectSlotsByName(Upload)

    def retranslateUi(self, Upload):
        Upload.setWindowTitle(_translate("Upload", "Shapefile hochladen", None))
        self.OK_button.setText(_translate("Upload", "OK", None))
        self.cancel_button.setText(_translate("Upload", "Abbrechen", None))
        self.upload_frame.setTitle(_translate("Upload", "Schritt 1", None))
        self.label.setText(_translate("Upload", "Zielschema", None))
        self.shapefile_browse_button.setText(_translate("Upload", "...", None))
        self.label_6.setText(_translate("Upload", "Shapefile", None))
        self.label_3.setText(_translate("Upload", "Projektion", None))
        self.label_2.setText(_translate("Upload", "Name", None))
        self.check_projection_button.setText(_translate("Upload", "Projektion prüfen", None))
        self.upload_button.setText(_translate("Upload", "Hochladen", None))
        self.identifiers_frame.setTitle(_translate("Upload", "Schritt 2", None))
        self.label_5.setText(_translate("Upload", "Wählen Sie die Spalte mit den Gebietsnamen aus.", None))
        self.label_4.setText(_translate("Upload", "Wählen Sie eine Spalte für die eindeutige Identifizierung der Gebiete aus.", None))

