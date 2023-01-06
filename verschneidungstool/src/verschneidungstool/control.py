# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, uic, QtWidgets, Qt
import os
import psycopg2

from verschneidungstool.main_view import Ui_MainWindow
from verschneidungstool.model import DBConnection
from verschneidungstool.dialogs import ConfigDialog, UploadAreaDialog, ExecDownloadResultsShape, IntersectionDialog, DownloadTablesDialog, check_status, get_selected
from verschneidungstool.connection import Login
from verschneidungstool.config import Config

config = Config()

UI_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'ui')


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    project_changed = QtCore.pyqtSignal()
    ui_file = 'PyQt/main.ui'

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        header = QtWidgets.QTreeWidgetItem(["Kategorie","Beschreibung"])
        self.structure_tree.setHeaderItem(header)
        self.structure_tree.itemClicked.connect(check_status)
        self.add_layer_button.clicked.connect(self.upload_area_shape)
        #self.add_stations_button.clicked.connect(self.upload_station_shape)
        self.delete_layer_button.clicked.connect(self.remove_area)
        #self.delete_stations_button.clicked.connect(self.remove_stations)
        self.intersect_button.clicked.connect(self.intersect)
        self.download_tables_button.clicked.connect(self.download_tables)
        # workaround: QT-Designer always sets this button to disabled, ignoring settings
        self.intersect_button.setEnabled(True)
        self.download_tables_button.setEnabled(True)

        self.results_button.clicked.connect(self.download_results)

        # connect the menu
        self.actionBeenden.triggered.connect(QtWidgets.qApp.quit)
        self.actionEinstellungen.triggered.connect(self.edit_settings)

        self.layer_combo.currentIndexChanged['QString'].connect(self.area_changed)
        #self.stations_combo.currentIndexChanged['QString'].connect(self.station_changed)
        self.scenario_combo.currentIndexChanged['QString'].connect(self.render_structure)

        self.dbconnect_button.clicked.connect(self.db_reset)

    def closeEvent(self, event):
        layer = self.layer_combo.currentText()
        config.settings['recent']['aggregations'] = layer
        #stations = self.stations_combo.currentText()
        #config.settings['recent']['stations'] = stations
        scenario = self.scenario_combo.currentText()
        config.settings['recent']['scenario'] = scenario
        config.write()
        return super().closeEvent(event)

    # check command-line arguments, if something shall be done automatically (without further user input)
    def exec_arguments(self, arguments):
        self.arguments = arguments

        if not arguments.upload and not arguments.intersection and not arguments.download:
            return

        #connect automatically
        if not self.db_reset():
            self.close()
            exit(1)

        if arguments.upload:
            auto_args = {
                'shape_path': arguments.shape_path,
                'schema': arguments.schema,
                'table_name': arguments.table_name,
                'srid': arguments.srid,
                'c_id': arguments.c_id,
                'c_name': arguments.c_name
            }
            self.upload_area_shape(auto_args=auto_args)

        if arguments.intersection:
            auto_args = {
                'schema': arguments.schema,
                'table_name': arguments.table_name,
            }
            self.intersect(auto_args)

        if arguments.download:
            auto_args = {
                'schema': arguments.schema,
                'table_name': arguments.table_name,
                'download_file': arguments.download_file,
                'scenario': arguments.scenario
            }
            self.download_results(auto_args)

        self.close()
        exit(1)

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

        db_config =  config.settings['db_config']
        self.login = Login(host=db_config['host'], port=db_config['port'],
                           user=db_config['username'],
                           password=db_config['password'],
                           db=db_config['db_name'])
        self.db_conn = DBConnection(login=self.login)

        # render main attributes
        if not self.refresh_attr(['schemata']):
            return False
        #if not self.render_stations():
            #return False
        if not self.render_areas():
            return False
        if not self.render_scenarios():
            return False

        # you only get here, if no errors occured
        self.main_frame.setEnabled(True)
        self.download_frame.setEnabled(True)
        self.download_tables_frame.setEnabled(True)
        self.intersect_frame.setEnabled(True)
        self.dbconnect_button.setText('Verbindung erneuern')
        return True

    def render_areas(self):
        self.layer_combo.clear()
        if not self.refresh_attr(['areas']):
            return False
        for (id, area_name, schema, table_name, can_be_deleted,
             check_last_calculation) in self.areas:
            self.layer_combo.addItem(
                area_name,
                [id, schema, table_name, can_be_deleted,
                 check_last_calculation])

        layer = config.settings['recent']['aggregations']
        self.layer_combo.setCurrentText(layer)
        self.area_changed()
        #stations = config.settings['recent']['stations']
        #self.stations_combo.setCurrentText(stations)
        #self.station_changed()
        return True

    def render_scenarios(self):
        self.scenario_combo.clear()
        if not self.refresh_attr(['scenarios']):
            return False
        for scenario, in self.scenarios:
            self.scenario_combo.addItem(str(scenario))
        scenario = config.settings['recent']['scenario']
        self.scenario_combo.setCurrentText(scenario)

        self.render_structure()
        return True

    '''
    query the main attributes from the db,
    gui elements will be disabled on error
    @param attributes list of attribute-names to be queried ('areas',
    'scenarios' or 'schemata')
    @return True, if successful, else False
    '''
    def refresh_attr(self, attributes):
        try:
            for attr in attributes:
                if attr == 'areas':
                    self.areas = self.db_conn.get_areas_available()
                if attr == 'scenarios':
                    self.scenarios = self.db_conn.get_scenarios_available()
                if attr == 'schemata':
                    self.schemata = self.db_conn.get_schemata_available()
            return True
        except Exception as e:
            msgBox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!",
                "Fehler bei der Verbindung zur Datenbank!\n\n" + str(e))
            msgBox.exec_()
            # disable all elements on exception
            self.main_frame.setEnabled(False)
            self.intersect_frame.setEnabled(False)
            self.download_frame.setEnabled(False)
            self.download_tables_frame.setEnabled(False)
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
        selected_data = self.layer_combo.itemData(idx)
        can_be_deleted = selected_data[3]
        check_last_calculation = selected_data[4]

        if can_be_deleted:
            self.delete_layer_button.setEnabled(True)
        else:
            self.delete_layer_button.setEnabled(False)

        if not check_last_calculation:
            self.intersect_frame.setEnabled(False)
        else:
            self.intersect_frame.setEnabled(True)

    '''
    initiate removal of the selected area (aggregation layer) from the database
    '''
    def remove_area(self):
        name = self.layer_combo.currentText()
        selected_data = self.layer_combo.itemData(
            self.layer_combo.currentIndex())
        can_be_deleted = selected_data[3]
        # do nothing, if area can't be deleted (you shouldn't get here anyway,
        # because button is disabled)
        if not can_be_deleted:
            return

        id, c = selected_data[0]
        schema = selected_data[1]
        table_name = selected_data[2]
        success, msg= self.db_conn.drop_area(id, table_name, schema)
        if success:
            msgBox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Erfolg", msg)
            msgBox.exec_()
        else:
            msgBox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!", msg)
            msgBox.exec_()

        self.render_areas()

    def render_structure(self):
        '''
        fill the tree view with categories and subcategories depending on
        year of the scenario selection
        '''
        idx = self.scenario_combo.currentIndex()
        # nothing selected (e.g. when triggered on clearance)
        if idx < 0:
            return
        self.structure_tree.clear()
        scenario = str(self.scenario_combo.currentText())
        year = self.db_conn.get_year_of_scenario(scenario)[0].year
        groups = self.db_conn.get_structure_groups_available(year)
        for group, structure in groups.items():
            group_item = QtWidgets.QTreeWidgetItem(self.structure_tree, [group])
            group_item.setCheckState(0, QtCore.Qt.Unchecked)
            group_item.setFlags(QtCore.Qt.ItemIsUserCheckable
                                | QtCore.Qt.ItemIsEnabled)
            for cat, cols in structure.items():
                cat_item = QtWidgets.QTreeWidgetItem(group_item, [cat])
                cat_item.setCheckState(0, QtCore.Qt.Unchecked)
                cat_item.setFlags(QtCore.Qt.ItemIsUserCheckable
                                  | QtCore.Qt.ItemIsEnabled)
                for col in cols:
                    col_item = QtWidgets.QTreeWidgetItem(cat_item, [col['name']])
                    col_item.setText(1, col['description'])
                    col_item.setCheckState(0, QtCore.Qt.Unchecked)
                    col_item.setFlags(QtCore.Qt.ItemIsUserCheckable
                                      | QtCore.Qt.ItemIsEnabled)
        self.structure_tree.resizeColumnToContents(0)

    def edit_settings(self):
        diag = ConfigDialog(self)  #, on_change=self.dbreset)

    def intersect(self, auto_args):

        last_calc = self.db_conn.get_last_calculated()
        auto_close = False

        if len(last_calc) > 0 and not last_calc[0].finished:
            msgBox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!",
                'Derzeit scheint bereits eine Berechnung stattzufinden!\n'
                'Bitte warten Sie, bis diese abgeschlossen ist.\n\n'
                'Wenn Sie sich sicher sind, dass alle Berechnungen bereits '
                'abgeschlossen sind, können Sie eine neue Berechnung '
                'erzwingen.')

            msgBox.addButton(QtWidgets.QPushButton('Berechnung erzwingen'),
                             QtWidgets.QMessageBox.YesRole)
            msgBox.addButton(QtWidgets.QPushButton('Abbrechen'),
                             QtWidgets.QMessageBox.NoRole)
            reply = msgBox.exec_()

            # 2nd button clicked (==No)
            if reply == 1:
                return
            self.db_conn.force_reset_calc()

        if not auto_args:
            item = self.layer_combo.itemData(
                self.layer_combo.currentIndex())
            schema = str(item[1])
            table = str(item[2])
        else:
            schema = auto_args['schema']
            table = auto_args['table_name']
            auto_close = True

        intersectDiag = IntersectionDialog(self.db_conn, schema,
                                           table, auto_close=auto_close)
        intersectDiag.exec_()


    def upload_area_shape(self, auto_args = None):
        schemata = [r.name for r in self.schemata]
        reserved_names = [self.layer_combo.itemText(i)
                          for i in range(self.layer_combo.count())]

        #if successfully uploaded, select last area = new area (important:
        # on_finish has to be executed first!)
        def on_success():
            self.layer_combo.setCurrentIndex(self.layer_combo.count() - 1)

        upDiag = UploadAreaDialog(self.db_conn, schemata, parent=self,
                                  on_finish=self.render_areas,
                                  reserved_names=reserved_names,
                                  on_success=on_success, auto_args=auto_args)

    def download_tables(self):
        downloadDialog = DownloadTablesDialog(self.db_conn, parent=self)

    def download_results(self, auto_args):
        if auto_args:
            get_all = True
        else:
            get_all = False
        selected_columns = [(i.text(0), i.parent().text(0))
            for i in get_selected(self.structure_tree, get_all)]
        last_calc = self.db_conn.get_last_calculated()

        selected_area = self.layer_combo.currentText()
        idx = self.layer_combo.currentIndex()
        selected_data = self.layer_combo.itemData(idx)
        check_last_calculation = selected_data[4]

        if check_last_calculation and not last_calc[0].finished:
            msgBox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!",
                'Derzeit scheint bereits eine Berechnung stattzufinden!\n'
                'Bitte warten Sie, bis diese abgeschlossen ist.\n\n'
                'Wenn Sie sich sicher sind, dass alle Berechnungen bereits '
                'abgeschlossen sind, können Sie die Ergebnisse dennoch '
                'herunterladen.')

            msgBox.addButton(QtWidgets.QPushButton('Herunterladen erzwingen'),
                             QtWidgets.QMessageBox.YesRole)
            msgBox.addButton(QtWidgets.QPushButton('Abbrechen'),
                             QtWidgets.QMessageBox.NoRole)
            reply = msgBox.exec_()
            # 2nd button clicked (==No)
            if reply == 1:
                return

        if not auto_args:
            if len(selected_columns) == 0:
                msg_box = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning, "Warnung!",
                    'Sie haben keine Kategorie ausgewählt!\n'
                    'Bitte wählen sie eine oder mehrere aus,\n'
                    'um zugehörige Daten zu erhalten.')
                msg_box.exec_()
                return

            schema = selected_data[1]
            table = selected_data[2]
            #results_schema = selected_data[5]
            #results_table = selected_data[6]
            scenario = str(self.scenario_combo.currentText())
            #station_idx = self.stations_combo.currentIndex()
            #station_table = self.stations_combo.currentText()
            #station_schema = self.stations_combo.itemData(station_idx)[1]

        else:
            selected_area = table = auto_args['table_name']
            schema = auto_args['schema']
            scenario = auto_args['scenario']

        if len(last_calc) == 0:
            msg_box = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!",
                'Es liegen keine verschnittenen Daten vor.\n\n'
                'Sie müssen neu verschneiden!')
            msg_box.exec_()
            return


        if check_last_calculation and (
            last_calc[0].area_name != selected_area or
            last_calc[0].schema != schema):
            msg_box = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Warning, "Warnung!",
                'Es liegen keine verschnittenen Daten für die '
                'gewählte Aggregationsstufe\n'
                '"{area}" ({schema}.{table}) vor.\n\n'.format(
                    area=selected_area, schema=schema, table=table) +
                'Sie müssen neu verschneiden!')
            msg_box.exec_()
            return

        # set scenario (referenced by db-view on results)
        self.db_conn.set_current_scenario(scenario)

        schema_resulttables = set(self.db_conn.get_column_definition(col, parent)['resulttable']
                                  for col, parent in selected_columns)

        several_resulttables = len(schema_resulttables) > 1

        csv = shp = xlsx = tra = False

        auto_close = False

        if not auto_args:
            recent_dirname = config.settings['recent'].get(
                'download_results_folder', '')
            if self.csv_radio_button.isChecked():
                fname = os.path.join(recent_dirname, 'results.csv')
                filename, ext = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Speichern unter', fname, '*.csv')
                if len(filename) > 0:
                    csv = True

            elif self.excel_radio_button.isChecked():
                fname = os.path.join(recent_dirname, 'results.xlsx')
                filename, ext = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Speichern unter', fname, '*.xlsx')
                if len(filename) > 0:
                    xlsx = True

            elif self.shape_radio_button.isChecked():
                fname = os.path.join(recent_dirname, 'results.shp')
                filename, ext = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Speichern unter', fname, '*.shp')
                if len(filename) > 0:
                    shp = True

            elif self.visum_radio_button.isChecked():
                mod_no = self.visum_mod_input.value()
                fname = os.path.join(recent_dirname, f'M{mod_no:06d}.tra')
                filename, ext = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Speichern unter', fname, '*.tra')
                if len(filename) > 0:
                    tra = True

            download_results_folder = os.path.split(filename)[0]
            config.settings['recent']['download_results_folder'] = download_results_folder

        else:
            auto_close = True
            filename = auto_args['download_file']
            f, extension = os.path.splitext(filename)
            if extension == '.csv':
                csv = True
            elif extension == '.xlsx':
                xlsx = True
            elif extension == '.shp':
                shp = True
            elif extension == '.tra':
                tra = True
            else:
                msg_box = QtWidgets.QMessageBox(
                    QtWidgets.QMessageBox.Warning, "Warnung!",
                    "Angegebene Dateiendung wird nicht unterstützt!")
                msg_box.exec_()
                return

        if csv or xlsx or tra:

            msg_box = QtWidgets.QMessageBox(parent=self)
            msg_box.setWindowTitle("Lade herunter, bitte warten ...")
            msg_box.setText("Daten werden heruntergeladen, Bitte warten ...")
            msg_box.setWindowModality(QtCore.Qt.NonModal)
            msg_box.show()

        resulttables_available = {r.schema_table: r
                                  for r in self.db_conn.get_resulttables_available()}

        for i, schema_resulttable in enumerate(schema_resulttables):
            append = i > 0
            results_schema, results_table = schema_resulttable.split('.')
            results_schema = results_schema.strip('"')
            results_table = results_table.strip('"')

            columns_for_resulttable = [
                colname for colname, parent in selected_columns
                if self.db_conn.get_column_definition(colname, parent)['resulttable']
                == schema_resulttable]
            visum_classname = resulttables_available[schema_resulttable].visum_class
            long_format = resulttables_available[schema_resulttable].long_format
            if several_resulttables:
                fp, ext = os.path.splitext(filename)
                fn = f'{fp}_{visum_classname}{ext}'
            else:
                fn = filename

            if csv:
                self.db_conn.results_to_csv(results_schema, results_table,
                                            columns_for_resulttable, fn)
            elif xlsx:
                self.db_conn.results_to_excel(results_schema, results_table,
                                              columns_for_resulttable, filename,
                                              visum_classname, append)
            elif tra:
                self.db_conn.results_to_visum_transfer(results_schema,
                                                       results_table,
                                                       columns_for_resulttable,
                                                       filename,
                                                       visum_classname,
                                                       append,
                                                       long_format)
            elif shp:
                diag = ExecDownloadResultsShape(
                    self.db_conn, results_schema, results_table, columns_for_resulttable,
                    fn, parent=self, auto_close=auto_close)
                diag.exec_()

        if csv or xlsx or tra:
            msg_box.close()
