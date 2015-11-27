# -*- coding: utf-8 -*-
from verschneidungstool.main_view import Ui_MainWindow
from verschneidungstool.model import DBConnection
from verschneidungstool.dialogs import SettingsDialog, UploadDialog, ExecShapeDownload, IntersectionDialog
from extractiontools.connection import Login
from PyQt4 import QtGui, QtCore
from verschneidungstool.config import Config

config = Config()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    project_changed = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        header = QtGui.QTreeWidgetItem(["Kategorie","Beschreibung"])
        self.structure_tree.setHeaderItem(header)
        self.structure_tree.itemClicked.connect(self.check_status)
        self.add_layer_button.clicked.connect(self.upload_shape)
        self.delete_layer_button.clicked.connect(self.remove_area)
        self.intersect_button.clicked.connect(self.intersect)
        # workaround: QT-Designer always sets this button to disabled, ignoring settings
        self.intersect_button.setEnabled(True)

        self.results_button.clicked.connect(self.download_results)

        # connect the menu
        self.actionBeenden.triggered.connect(QtGui.qApp.quit)
        self.actionEinstellungen.triggered.connect(self.edit_settings)

        self.layer_combo.currentIndexChanged['QString'].connect(self.area_changed)
        self.year_combo.currentIndexChanged['QString'].connect(self.view_structure)

        self.dbconnect_button.clicked.connect(self.db_reset)

    '''
    connect to the database and initiate rendering of it's contents
    '''
    def db_reset(self):
        # clear view
        self.structure_tree.clear()
        self.delete_layer_button.setEnabled(False)
        self.intersect_frame.setEnabled(False)

        ## disable while loading (just to show user, that loading is in progress)
        #self.main_frame.setEnabled(False)

        db_config = config.settings['db_config']
        self.login = Login(host=db_config['host'], port=db_config['port'],
                           user=db_config['username'], password=db_config['password'],
                           db=db_config['db_name'])
        self.db_conn = DBConnection(login=self.login)

        # render main attributes
        if not self.refresh_attr(['schemata']):
            return
        if not self.render_areas():
            return
        if not self.render_years():
            return

        # you only get here, if no errors occured
        self.main_frame.setEnabled(True)
        self.download_frame.setEnabled(True)
        self.intersect_frame.setEnabled(True)
        self.dbconnect_button.setText('Verbindung erneuern')

    def render_areas(self):
        self.layer_combo.clear()
        if not self.refresh_attr(['areas']):
            return False
        for id, area_name, schema, table_name, can_be_deleted in self.areas:
            self.layer_combo.addItem(area_name, [id, schema, table_name, can_be_deleted])

        self.area_changed()
        return True

    def render_years(self):
        self.year_combo.clear()
        if not self.refresh_attr(['years']):
            return False
        for year, in self.years:
            self.year_combo.addItem(str(year))

        self.view_structure()
        return True

    '''
    query the main attributes from the db,
    gui elements will be disabled on error
    @param attributes list of attribute-names to be queried ('areas', 'years' or 'schemata')
    @return True, if successful, else False
    '''
    def refresh_attr(self, attributes):
        try:
            for attr in attributes:
                if attr == 'areas':
                    self.areas = self.db_conn.get_areas_available()
                if attr == 'years':
                    self.years = self.db_conn.get_years_available()
                if attr == 'schemata':
                    self.schemata = self.db_conn.get_schemata_available()
            return True
        except Exception as e:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8("Fehler bei der Verbindung zur Datenbank!"))
            msgBox.exec_()
            # disable all elements on exception
            self.main_frame.setEnabled(False)
            self.intersect_frame.setEnabled(False)
            self.download_frame.setEnabled(False)
            self.dbconnect_button.setText('mit Datenbank verbinden')
            return False


    '''
    enable/disable delete button depending on whether area can be deleted or not
    '''
    def area_changed(self):
        idx = self.layer_combo.currentIndex()
        # nothing selected (e.g. when triggered on clearance)
        if idx < 0:
            return
        can_be_deleted = self.layer_combo.itemData(idx).toList()[3].toBool()
        if can_be_deleted:
            self.delete_layer_button.setEnabled(True)
        else:
            self.delete_layer_button.setEnabled(False)

    '''
    initiate removal of the selected area (aggregation layer) from the database
    '''
    def remove_area(self):
        name = self.layer_combo.currentText()
        selected_data = self.layer_combo.itemData(self.layer_combo.currentIndex()).toList()
        can_be_deleted = selected_data[3].toBool()
        # do nothing, if area can't be deleted (you shouldn't get here anyway, because button is disabled)
        if not can_be_deleted:
            return

        id, c = selected_data[0].toInt()
        schema = selected_data[1].toString()
        table_name = selected_data[2].toString()
        success = self.db_conn.drop_area(id, table_name, schema)
        if success:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Erfolg",
                                       _fromUtf8("Löschen der Aggregationsstufe {} war erfolgreich.".format(name)))
            msgBox.exec_()
        else:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8("Beim Löschen der Aggregationsstufe {} ist ein Fehler aufgetreten!".format(name)))
            msgBox.exec_()

        self.render_areas()


    '''
    fill the tree view with categories and subcategories depending on year selection
    '''
    def view_structure(self):
        idx = self.year_combo.currentIndex()
        # nothing selected (e.g. when triggered on clearance)
        if idx < 0:
            return
        self.structure_tree.clear()
        year = str(self.year_combo.currentText())
        structure = self.db_conn.get_structure_available(year)
        for cat, cols in structure.iteritems():
            cat_item = QtGui.QTreeWidgetItem(self.structure_tree, [cat])
            cat_item.setCheckState(0,QtCore.Qt.Unchecked)
            cat_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            for col in cols:
                col_item = QtGui.QTreeWidgetItem(cat_item, [col])
                col_item.setCheckState(0,QtCore.Qt.Unchecked)
                col_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.structure_tree.resizeColumnToContents(0)

    '''
    check the check-status of the item inside the tree view
    and accordingly update the check-status of it's parent / siblings
    '''
    def check_status(self, item):
        parent = item.parent()
        # given item is sub-category -> check/uncheck/partial check of parent of given item, depending on number of checked children
        if(parent):
            child_count = parent.childCount()
            checked_count = 0
            for i in range(child_count):
                if (parent.child(i).checkState(0) == QtCore.Qt.Checked):
                    checked_count += 1
            if checked_count == 0:
                parent.setCheckState(0, QtCore.Qt.Unchecked)
            elif checked_count == child_count:
                parent.setCheckState(0, QtCore.Qt.Checked)
            else:
                parent.setCheckState(0, QtCore.Qt.PartiallyChecked)
        # given item is category -> check or uncheck all children
        elif item.checkState(0) != QtCore.Qt.PartiallyChecked:
            state = item.checkState(0)
            child_count = item.childCount()
            for i in range(child_count):
                item.child(i).setCheckState(0, state)

    '''
    returns a list of all checked sub-categories in the tree view
    '''
    def get_selected(self):
        root = self.structure_tree.invisibleRootItem()
        cat_count = root.childCount()
        checked = []
        # iterate categories
        for i in range(cat_count):
            cat_item = root.child(i)
            col_count = cat_item.childCount()
            # get checked sub-categories
            for j in range(col_count):
                col_item = cat_item.child(j)
                if(col_item.checkState(0) == QtCore.Qt.Checked):
                    checked.append(str(col_item.text(0)))
        return checked

    def edit_settings(self):
        diag = SettingsDialog(self)  #, on_change=self.dbreset)

    def intersect(self):

        last_calc = self.db_conn.get_last_calculated()

        if len(last_calc) > 0 and not last_calc[0].finished:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8('Derzeit findet bereits eine Berechnung statt!\n' +
                                                 'Bitte warten Sie, bis diese abgeschlossen ist.'))
            msgBox.exec_()
            return

        item = self.layer_combo.itemData(self.layer_combo.currentIndex()).toList()
        schema = str(item[1].toString())
        table = str(item[2].toString())
        intersectDiag = IntersectionDialog(self.db_conn, schema, table)
        intersectDiag.exec_()


    def upload_shape(self):
        schemata = [r.name for r in self.schemata]
        reserved_names = [self.layer_combo.itemText(i) for i in range(self.layer_combo.count())]

        #if successfully uploaded, select last area = new area (important: on_finish has to be executed first!)
        def on_success():
            self.layer_combo.setCurrentIndex(self.layer_combo.count() - 1)

        upDiag = UploadDialog(self.db_conn, schemata, parent=self, on_finish=self.render_areas,
                              reserved_names=reserved_names, on_success=on_success)
        upDiag.exec_()


    def download_results(self):
        selected_columns = self.get_selected()

        if len(selected_columns) == 0:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8('Sie haben keine Kategorie ausgewählt!\n' +
                                                 'Bitte wählen sie eine oder mehrere aus,\n' +
                                                 'um zugehörige Daten zu erhalten.'))
            msgBox.exec_()
            return

        selected_area = self.layer_combo.currentText()
        idx = self.layer_combo.currentIndex()
        schema = self.layer_combo.itemData(idx).toList()[1].toString()
        table = self.layer_combo.itemData(idx).toList()[2].toString()
        last_calc = self.db_conn.get_last_calculated()

        if not last_calc[0].finished:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8('Derzeit findet eine Berechnung statt!\n' +
                                                 'Bitte warten Sie, bis diese abgeschlossen ist.'))
            msgBox.exec_()
            return

        if len(last_calc) == 0 or last_calc[0].area_name != selected_area or last_calc[0].schema != schema:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8('Es liegen keine verschnittenen Daten für die gewählte Aggregationsstufe\n' +
                                                 '"{area}" ({schema}.{table}) vor.\n\n'.format(area=selected_area, schema=schema, table=table) +
                                                 'Sie müssen neu verschneiden!'))
            msgBox.exec_()
            return

        # set year (referenced by db-view on results)
        year = str(self.year_combo.currentText())
        self.db_conn.set_current_year(year)

        if self.csv_radio_button.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(
                self, _fromUtf8('Speichern unter'), 'results.csv', '*.csv')
            if len(filename) > 0:
                self.db_conn.results_to_csv(selected_columns, filename)

        if self.excel_radio_button.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(
                self, _fromUtf8('Speichern unter'), 'results.xls', '*.xls')
            if len(filename) > 0:
                self.db_conn.results_to_excel(selected_columns, filename)

        if self.shape_radio_button.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(
                self, _fromUtf8('Speichern unter'), 'results.shp', '*.shp')
            if len(filename) > 0:
                diag = ExecShapeDownload(
                    self.db_conn, selected_columns, filename, parent=self)

