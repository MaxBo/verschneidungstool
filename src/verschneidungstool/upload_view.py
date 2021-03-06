# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Upload(object):
    def setupUi(self, Upload):
        Upload.setObjectName("Upload")
        Upload.resize(550, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Upload.sizePolicy().hasHeightForWidth())
        Upload.setSizePolicy(sizePolicy)
        Upload.setMinimumSize(QtCore.QSize(550, 450))
        Upload.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Upload.setSizeGripEnabled(False)
        Upload.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Upload)
        self.verticalLayout.setObjectName("verticalLayout")
        self.upload_frame = QtWidgets.QGroupBox(Upload)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upload_frame.sizePolicy().hasHeightForWidth())
        self.upload_frame.setSizePolicy(sizePolicy)
        self.upload_frame.setObjectName("upload_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.upload_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.upload_layout = QtWidgets.QGridLayout()
        self.upload_layout.setObjectName("upload_layout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.schema_combo = QtWidgets.QComboBox(self.upload_frame)
        self.schema_combo.setObjectName("schema_combo")
        self.gridLayout_4.addWidget(self.schema_combo, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.upload_frame)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 2, 0, 1, 1)
        self.shapefile_edit = QtWidgets.QLineEdit(self.upload_frame)
        self.shapefile_edit.setObjectName("shapefile_edit")
        self.gridLayout_4.addWidget(self.shapefile_edit, 0, 1, 1, 1)
        self.shapefile_browse_button = QtWidgets.QPushButton(self.upload_frame)
        self.shapefile_browse_button.setMaximumSize(QtCore.QSize(30, 16777215))
        self.shapefile_browse_button.setObjectName("shapefile_browse_button")
        self.gridLayout_4.addWidget(self.shapefile_browse_button, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.upload_frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.upload_frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.upload_frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 5, 0, 1, 1)
        self.name_edit = QtWidgets.QLineEdit(self.upload_frame)
        self.name_edit.setObjectName("name_edit")
        self.gridLayout_4.addWidget(self.name_edit, 3, 1, 1, 1)
        self.projection_combo = QtWidgets.QComboBox(self.upload_frame)
        self.projection_combo.setEditable(False)
        self.projection_combo.setObjectName("projection_combo")
        self.gridLayout_4.addWidget(self.projection_combo, 5, 1, 1, 1)
        self.check_projection_button = QtWidgets.QPushButton(self.upload_frame)
        self.check_projection_button.setObjectName("check_projection_button")
        self.gridLayout_4.addWidget(self.check_projection_button, 5, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 4, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.encoding_combo = QtWidgets.QComboBox(self.upload_frame)
        self.encoding_combo.setObjectName("encoding_combo")
        self.horizontalLayout_3.addWidget(self.encoding_combo)
        self.custom_encoding_edit = QtWidgets.QLineEdit(self.upload_frame)
        self.custom_encoding_edit.setEnabled(False)
        self.custom_encoding_edit.setObjectName("custom_encoding_edit")
        self.horizontalLayout_3.addWidget(self.custom_encoding_edit)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.upload_frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.upload_layout.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.upload_button = QtWidgets.QPushButton(self.upload_frame)
        self.upload_button.setObjectName("upload_button")
        self.horizontalLayout.addWidget(self.upload_button)
        self.upload_layout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.message_edit = QtWidgets.QTextEdit(self.upload_frame)
        self.message_edit.setEnabled(True)
        self.message_edit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.message_edit.setReadOnly(True)
        self.message_edit.setObjectName("message_edit")
        self.upload_layout.addWidget(self.message_edit, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.upload_layout)
        self.verticalLayout.addWidget(self.upload_frame)
        self.identifiers_frame = QtWidgets.QGroupBox(Upload)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.identifiers_frame.sizePolicy().hasHeightForWidth())
        self.identifiers_frame.setSizePolicy(sizePolicy)
        self.identifiers_frame.setObjectName("identifiers_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.identifiers_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.select_ids_layout = QtWidgets.QGridLayout()
        self.select_ids_layout.setObjectName("select_ids_layout")
        self.pkey_combo = QtWidgets.QComboBox(self.identifiers_frame)
        self.pkey_combo.setObjectName("pkey_combo")
        self.select_ids_layout.addWidget(self.pkey_combo, 1, 1, 1, 1)
        self.names_combo = QtWidgets.QComboBox(self.identifiers_frame)
        self.names_combo.setObjectName("names_combo")
        self.select_ids_layout.addWidget(self.names_combo, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.identifiers_frame)
        self.label_4.setObjectName("label_4")
        self.select_ids_layout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.identifiers_frame)
        self.label_5.setObjectName("label_5")
        self.select_ids_layout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.identifiers_frame)
        self.label_7.setObjectName("label_7")
        self.select_ids_layout.addWidget(self.label_7, 4, 0, 1, 1)
        self.hst_combo = QtWidgets.QComboBox(self.identifiers_frame)
        self.hst_combo.setObjectName("hst_combo")
        self.select_ids_layout.addWidget(self.hst_combo, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.select_ids_layout.addItem(spacerItem2, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.select_ids_layout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.identifiers_frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.OK_button = QtWidgets.QPushButton(Upload)
        self.OK_button.setObjectName("OK_button")
        self.horizontalLayout_2.addWidget(self.OK_button)
        self.cancel_button = QtWidgets.QPushButton(Upload)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Upload)
        QtCore.QMetaObject.connectSlotsByName(Upload)

    def retranslateUi(self, Upload):
        _translate = QtCore.QCoreApplication.translate
        Upload.setWindowTitle(_translate("Upload", "Shapefile hochladen"))
        self.upload_frame.setTitle(_translate("Upload", "Schritt 1"))
        self.label.setText(_translate("Upload", "Zielschema"))
        self.shapefile_browse_button.setText(_translate("Upload", "..."))
        self.label_2.setText(_translate("Upload", "Name"))
        self.label_6.setText(_translate("Upload", "Shapefile"))
        self.label_3.setText(_translate("Upload", "Projektion"))
        self.check_projection_button.setText(_translate("Upload", "Projektion prüfen"))
        self.label_8.setText(_translate("Upload", "Encoding"))
        self.upload_button.setText(_translate("Upload", "Hochladen"))
        self.identifiers_frame.setTitle(_translate("Upload", "Schritt 2"))
        self.label_4.setText(_translate("Upload", "Wählen Sie eine Spalte für die eindeutige Identifizierung der Gebiete aus."))
        self.label_5.setText(_translate("Upload", "Wählen Sie die Spalte mit den Gebietsnamen aus."))
        self.label_7.setText(_translate("Upload", "Wählen Sie die Standard-Haltestellen für die Aggregation aus."))
        self.OK_button.setText(_translate("Upload", "OK"))
        self.cancel_button.setText(_translate("Upload", "Abbrechen"))

