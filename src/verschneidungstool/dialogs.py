# -*- coding: utf-8 -*-
from verschneidungstool.settings_view import Ui_Settings
from verschneidungstool.upload_view import Ui_Upload
from verschneidungstool.progress_view import Ui_ProgressDialog
from verschneidungstool.download_data_view import Ui_DownloadDataDialog
from PyQt4 import QtCore, QtGui
from verschneidungstool.config import Config, DEFAULT_SRID
from verschneidungstool.model import parse_projection_file, parse_projection_data
import copy, os, re

config = Config()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""

FINISHED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: green;
    width: 10px;
    margin: 1px;
}
"""

ABORTED_STYLE = """
QProgressBar{
    border: 2px solid red;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 10px;
    margin: 1px;
}
"""


'''
check the check-status of the item inside the tree view
and accordingly update the check-status of it's parent / siblings
'''
def check_status(item):
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
def get_selected(tree, get_all=False):
    root = tree.invisibleRootItem()
    cat_count = root.childCount()
    checked = []
    # iterate categories
    for i in range(cat_count):
        cat_item = root.child(i)
        col_count = cat_item.childCount()
        # get checked sub-categories
        for j in range(col_count):
            col_item = cat_item.child(j)
            if(get_all or col_item.checkState(0) == QtCore.Qt.Checked):
                checked.append(str(col_item.text(0)))
    return checked

def set_file(parent, line_edit, extension, do_split=False):
    '''
    open a file browser to put a path to a file into the given line edit
    '''
    try:
        current = os.path.split(str(line_edit.text()))[0]
    except:
        current = ''

    filename = str(
        QtGui.QFileDialog.getOpenFileName(
            parent, _fromUtf8('Datei wählen'), current+'/'+extension))
    if do_split:
        filename = os.path.split(filename)[0]

    # filename is '' if canceled
    if len(filename) > 0:
        line_edit.setText(filename)

def set_directory(parent, line_edit):
    dirname = str(
            QtGui.QFileDialog.getExistingDirectory(
                parent, _fromUtf8('Zielverzeichnis wählen')))
    # dirname is '' if canceled
    if len(dirname) > 0:
        line_edit.setText(dirname)

def validate_dbstring(string):
    '''
    validates if given string is valid for table- and column-names in databases (only small letters, digits and underscore allowed with trailing letter or underscore)
    return true if valid, else false
    '''
    pattern = '^[a-z_][a-z0-9_]*$'
    a = re.match(pattern, string)
    if (a):
        return True
    return False

class SettingsDialog(QtGui.QDialog, Ui_Settings):
    '''
    open a dialog to set the project name and folder and afterwards create
    a new project
    '''

    def __init__(self, parent=None, on_change=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.old_db_config = copy.deepcopy(config.settings['db_config'])
        self.login_changed = False
        self.on_change = on_change
        self.OK_button.clicked.connect(self.write_config)
        self.cancel_button.clicked.connect(self.close)

        self.psql_browse_button.clicked.connect(
            lambda: set_file(self, self.psql_edit, 'psql.exe'))
        self.shp2pgsql_browse_button.clicked.connect(
            lambda: set_file(self, self.shp2pgsql_edit, 'shp2pgsql.exe'))
        self.pgsql2shp_browse_button.clicked.connect(
            lambda: set_file(self, self.pgsql2shp_edit, 'pgsql2shp.exe'))

        self.srid_default_button.clicked.connect(
            lambda: self.srid_edit.setText(str(DEFAULT_SRID)))

        self.fill()
        self.show()

    def fill(self):
        '''
        fill form with values from stored config
        '''
        db_config = config.settings['db_config']
        self.username_edit.setText(db_config['username'])
        self.password_edit.setText(db_config['password'])
        self.dbname_edit.setText(db_config['db_name'])
        self.host_edit.setText(db_config['host'])
        self.port_edit.setText(db_config['port'])
        self.srid_edit.setText(db_config['srid'])

        env = config.settings['env']
        self.psql_edit.setText(env['psql_path'])
        self.shp2pgsql_edit.setText(env['shp2pgsql_path'])
        self.pgsql2shp_edit.setText(env['pgsql2shp_path'])

    def write_config(self):
        '''
        get values from form and write changed config to config singleton and to disk
        '''
        db_config = config.settings['db_config']
        db_config['username'] = str(self.username_edit.text())
        db_config['password'] = str(self.password_edit.text())
        db_config['db_name'] = str(self.dbname_edit.text())
        db_config['host'] = str(self.host_edit.text())
        db_config['port'] = str(self.port_edit.text())
        db_config['srid'] = str(self.srid_edit.text())

        env = config.settings['env']
        env['psql_path'] = str(self.psql_edit.text())
        env['shp2pgsql_path'] = str(self.shp2pgsql_edit.text())
        env['pgsql2shp_path'] = str(self.pgsql2shp_edit.text())

        config.write()
        self.close()

        # check if login changed (ToDo: trigger event?)
        shared_items = set(self.old_db_config.items()) & set(db_config.items())
        if self.on_change and (len(shared_items) != len(db_config)):
            self.on_change()


    def set_folder(self, line_edit):
        '''
        open a file browser to put a directory into the given line edit
        '''
        folder = str(
            QtGui.QFileDialog.getExistingDirectory(
                self, 'Ordner wählen', directory=line_edit.text()))
        # folder is '' if canceled
        if len(folder) > 0:
            line_edit.setText(folder)


class UploadShapeDialog(QtGui.QDialog, Ui_Upload):
    '''
    dialog for uploading shape files
    '''

    def __init__(self, db_connection, schemata, upload_function, parent=None, on_finish=None, reserved_names=None, on_success=None, auto_args=None):
        super(UploadShapeDialog, self).__init__(parent)
        self.parent = parent
        self.on_finish = on_finish
        self.on_success = on_success
        self.db_connection = db_connection
        self.reserved_names = reserved_names
        self.setupUi(self)
        self.auto_args = auto_args
        self.upload_function = upload_function

        projections_available = self.db_connection.get_projections_available()
        # add available projections to combobox
        for p in projections_available:
            self.projection_combo.addItem(
                _fromUtf8("{0} - {1}".format(p.srid, p.description)),
                # data: srid, description, not in database
                [p.srid, p.description, False])

        self.shapefile_browse_button.clicked.connect(self.set_shape)
        self.check_projection_button.clicked.connect(self.check_srid)
        self.check_projection_button.setEnabled(False)
        self.upload_button.clicked.connect(self.upload)
        self.cancel_button.clicked.connect(self.close)
        self.identifiers_frame.setDisabled(True)
        self.identifiers_frame.setHidden(True)
        self.schema_combo.addItems(schemata)
        self.OK_button.setDisabled(True)

        self.show()

        if auto_args:
            self.auto_start()

    def auto_start(self):
        shapefile = self.auto_args['shape_path']
        self.shapefile_edit.setText(shapefile)
        self.schema_combo.addItem(self.auto_args['schema'])
        srid = self.auto_args['srid']
        self.analyse_projection_file()
        name = self.auto_args['table_name']
        if not name:
            name = os.path.splitext(os.path.split(shapefile)[1])[0].lower()
        self.name_edit.setText(name)
        if(srid):
            idx = -1
            # find srid in the available projections
            for i in range(self.projection_combo.count()):
                s, c = self.projection_combo.itemData(i).toList()[0].toInt()
                if s == int(srid):
                    idx = i
                    break
            # select if found
            if idx >= 0:
                self.projection_combo.setCurrentIndex(idx)
            else:
                self.projection_combo.addItem(srid)
                self.projection_combo.setCurrentIndex(self.projection_combo.count() - 1)
        else:
            self.check_srid()

        self.upload()

        # identifiers
        if (self.auto_args['c_id']):
            self.pkey_combo.addItem(self.auto_args['c_id'])
        else:
            self.selection_canceled()
            return self.close()
        if (self.auto_args['c_name']):
            self.pkey_combo.addItem(self.auto_args['c_name'])

        self.set_zone()
        self.close()

    def set_shape(self):
        set_file(self, self.shapefile_edit, '*.shp')
        shapefile = str(self.shapefile_edit.text())
        name = self.name_edit.text()
        if(len(name) == 0):
            try:
                # take filename without extension as name, if none is set yet
                self.name_edit.setText(os.path.splitext(os.path.split(shapefile)[1])[0].lower())
            except:
                pass
        self.analyse_projection_file()

    '''
    upload the shape-file
    '''
    def upload(self):
        projection = self.projection_combo.itemData(self.projection_combo.currentIndex()).toList()
        srid, can_convert = projection[0].toInt()
        desc = str(projection[1].toString())
        proj_not_in_db = projection[2].toBool()
        shapefile = str(self.shapefile_edit.text())
        self.schema = self.schema_combo.currentText()
        self.name = self.name_edit.text()
        if not os.path.exists(shapefile):
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       "Die angegebene Datei existiert nicht!")
            msgBox.exec_()
            return False
        if not validate_dbstring(self.name):
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Warnung!',
                                       'Der angegebene Name entspricht nicht\n' +
                                       _fromUtf8('dem für Tabellennamen geforderten Muster\n') +
                                       '"^[a-z_][a-z0-9_]*$"\n' +
                                       '(nur Kleinbuchstaben, Ziffern und Unterstrich erlaubt)')
            msgBox.exec_()
            return False

        if self.reserved_names:
            for r in self.reserved_names:
                if self.name == r:
                    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                               "Der Name '{}' ist bereits vergeben!".format(self.name))
                    msgBox.exec_()
                    return False

        if proj_not_in_db:
            self.db_connection.add_projection(srid, desc)
        if self.auto_args:
            auto_close = True
        else:
            auto_close = False
        self.upload_diag = ExecUploadShape(self.db_connection, self.schema, self.name, shapefile, self.upload_function,
                                      parent=self, srid=srid, on_finish=self.on_finish, on_success=self.on_success, auto_close=auto_close)
        self.upload_diag.exec_()
        return True

    '''
    check for a .prj corresponding to the selected shapefile and get the description of the projection
    '''
    def analyse_projection_file(self):
        shapefile = str(self.shapefile_edit.text())

        if len(shapefile) == 0:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8("Sie müssen zunächst ein shapefile auswählen!"))
            msgBox.exec_()
            return

        prj_file = os.path.splitext(shapefile)[0] + '.prj'
        if not os.path.exists(prj_file):
            message = 'Keine zugehörige .prj-Datei gefunden!'

        else:
            self.proj_data, projcs, geogcs = parse_projection_file(prj_file)
            message = '<i>{} analysiert</i> <br>'.format(prj_file)
            message += 'PROJCS: {} <br>'.format(projcs)
            message += 'GEOGCS: {} <br>'.format(geogcs)
            self.check_projection_button.setEnabled(True)

        self.message_edit.setHtml(message)

    '''
    check database for a matching srid to the read projection data
    '''
    def check_srid(self):
        srid = None
        try:
            srid = self.db_connection.get_srid(self.proj_data)[0].prjtxt2epsg
            message = 'Projektion entspricht der srid <b>{}</b> '.format(srid)
        except:
            message = '<b>Es konnte keine passende srid bestimmt werden!<b> <br>'

        self.check_projection_button.setEnabled(False)

        if srid:
            idx = -1
            # find srid in the available projections
            for i in range(self.projection_combo.count()):
                s, c = self.projection_combo.itemData(i).toList()[0].toInt()
                if s == srid:
                    idx = i
                    break

            # select if found
            if idx >= 0:
                description = self.projection_combo.itemData(idx).toList()[1].toString()
                message += '<b>- {}</b><br>'.format(description)
                self.projection_combo.setCurrentIndex(idx)

            # projection is not available yet -> check db if it is supported and add projection
            else:
                entries = self.db_connection.get_spatial_ref(srid)
                if len(entries) == 0:
                    message += _fromUtf8('<br> <b> <i> srid {} wird nicht unterstützt!</i> </b><br>').format(srid)
                else:
                    projcs, geogcs = parse_projection_data(entries[0].srtext)
                    description = projcs if projcs else geogcs
                    message += '<b>- {}</b><br>'.format(description)
                    message += _fromUtf8('<i> Projektion ist noch nicht in der Datenbank vorhanden, wird beim Hochladen hinzugefügt </i>'.format(description))
                    # add new srid to combobox and select it
                    self.projection_combo.addItem(
                        _fromUtf8("{0} - {1}".format(srid, description)),
                        [srid, description, True])  # flag: not in database yet
                    self.projection_combo.setCurrentIndex(len(self.projection_combo) - 1)

        self.message_edit.append(message)


class UploadAreaDialog(UploadShapeDialog):
    '''
    dialog for uploading shapes to define areas, adds a second step (selecting identifiers) to UploadShapeDialog
    '''
    def __init__(self, db_connection, schemata, parent=None, on_finish=None, reserved_names=None, on_success=None, auto_args=None):
        upload_function = db_connection.add_area
        super(UploadAreaDialog, self).__init__(db_connection, schemata, upload_function, parent=parent, on_finish=on_finish, reserved_names=reserved_names, on_success=on_success, auto_args=auto_args)
        self.identifiers_frame.setHidden(False)
        self.OK_button.setDisabled(True)

    def upload(self):
        success = super(UploadAreaDialog, self).upload()
        if success and not self.auto_args:
            self.selectIdentifiers()

    def set_identifiers(self):
        # try to set zone with selected values, repeat if errors occure
        id_key = self.pkey_combo.currentText()
        name_key = self.names_combo.currentText()
        idx = self.hst_combo.currentIndex()
        hst_id = self.hst_combo.itemData(idx).toList()[0].toInt()[0]

        success, msg = self.db_connection.set_zone(self.schema, self.name, hst_id, zone_id_column=id_key, zone_name_column=name_key)

        if success:
            self.accept()
        else:
            msgBox = QtGui.QMessageBox(
                QtGui.QMessageBox.Warning, "Warnung!",
                "Es ist ein Fehler aufgetreten.\n" + '<b>{}</b>'.format(msg))
            msgBox.exec_()

    def set_default_stops(self):
        idx = self.hst_combo.currentIndex()
        def_stop_id = self.hst_combo.itemData(idx).toList()[0].toInt()

    '''
    removes all elements of this dialog and creates comboboxes to ask for id and name of newly created zone
    '''
    def selectIdentifiers(self):

        self.upload_frame.setDisabled(True)
        for id, name, schema, can_be_deleted in self.db_connection.get_stations_available():
            self.hst_combo.addItem(name, [id])

        key_columns = self.db_connection.get_column_names(self.schema, self.name)
        # remove column geom, this one shouldn't become pkey
        key_columns = [col.column_name for col in key_columns if col.column_name != 'geom']
        # selection for names is same list with leading empty element
        name_columns = [''] + copy.deepcopy(key_columns)

        self.pkey_combo.addItems(key_columns)
        self.names_combo.addItems(name_columns)

        self.identifiers_frame.setDisabled(False)
        self.OK_button.clicked.connect(self.set_identifiers)
        self.cancel_button.setDisabled(True)
        self.OK_button.setDisabled(False)

class UploadStationDialog(UploadShapeDialog):
    '''
    dialog for uploading shapes to add stations (no second step)
    '''
    def __init__(self, db_connection, schemata, parent=None, on_finish=None, reserved_names=None, on_success=None, auto_args=None):
        upload_function = db_connection.add_stations
        super(UploadStationDialog, self).__init__(db_connection, schemata, upload_function, parent=parent, on_finish=on_finish, reserved_names=reserved_names, on_success=on_success, auto_args=auto_args)
        self.name_edit.setDisabled(True)

    def upload(self):
        success = super(UploadStationDialog, self).upload()
        if success:
            self.upload_frame.setDisabled(True)
            self.OK_button.setDisabled(False)
            self.OK_button.clicked.connect(self.close)
            self.cancel_button.setDisabled(True)

class SelectDialog(QtGui.QDialog):
    '''
    executable dialog for getting an item out of a combobox with the given items,
    creates mutliple comboboxes if items is list of lists
    get the selected value with get_selection()
    '''
    def __init__(self, title, labels, items, parent=None):
        if not isinstance(labels, list): labels = [labels]
        if not isinstance(items[0], list): items = [items]

        super(SelectDialog, self).__init__(parent)
        self.setWindowTitle(title)

        layout = QtGui.QVBoxLayout(self)
        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.combo_boxes = []

        for i, item in enumerate(items):
            if len(labels) > i:
                layout.addWidget(QtGui.QLabel(labels[i]))

            combo_box = QtGui.QComboBox()
            combo_box.addItems(item)
            layout.addWidget(combo_box)
            self.combo_boxes.append(combo_box)
            layout.addItem(spacer)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        layout.addWidget(self.buttons)

    def get_selections(self):
        ret = []
        for combo in self.combo_boxes:
            ret.append(str(combo.currentText()))
        return ret


class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog):
    """
    Dialog showing progress in textfield and bar after starting a certain task with run()
    """
    def __init__(self, parent=None, auto_close=False):
        super(ProgressDialog, self).__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.progress_bar.setStyleSheet(DEFAULT_STYLE)
        self.progress_bar.setValue(0)
        self.cancelButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.run)
        self.auto_close = auto_close

    def running(self):
        self.startButton.setEnabled(False)
        self.cancelButton.setText('Stoppen')
        self.cancelButton.clicked.disconnect(self.close)

    def stopped(self):
        self.startButton.setEnabled(True)
        self.cancelButton.setText(_fromUtf8('Schließen'))
        self.cancelButton.clicked.connect(self.close)
        if self.auto_close:
            self.close()

    def show_status(self, text, progress=None):
        if hasattr(text, 'toLocal8Bit'):
            text = str(text.toLocal8Bit())
        else:
            text = _fromUtf8(text)
        self.log_edit.insertHtml(text + '<br>')
        self.log_edit.moveCursor(QtGui.QTextCursor.End)
        if progress:
            if isinstance(progress, QtCore.QVariant):
                progress = progress.toInt()[0]
            self.progress_bar.setValue(progress)

    # task needs to be overridden
    def run(self):
        pass

class IntersectionDialog(ProgressDialog):
    """
    ProgressDialog extented by an internal thread for intersecting
    """
    def __init__(self, db_connection, schema, table, parent=None, auto_close=False):
        super(IntersectionDialog, self).__init__(parent=parent, auto_close=auto_close)
        self.table = table
        self.schema = schema
        self.db_connection = db_connection
        # start intersection queries as a thread
        self.thread = db_connection.new_intersection(schema, table)

        # we don't need a start button at all
        self.startButton.hide()
        # we don't need a cancel button as well, you can't cancel the synchronous sql-queries (would mess up the database)
        self.cancelButton.hide()

        self.connect(self.thread, QtCore.SIGNAL("progress(QString, QVariant)"), self.show_status)
        self.thread.started.connect(self.running)
        self.thread.finished.connect(self.stopped)

        # start process directly (simulate click on start)
        self.startButton.clicked.emit(True)

    def run(self):
        self.thread.start()
        #success, msg = self.db_conn.new_intersection(schema, table, on_progress=show_status)
        #if not success:
            #msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Fehler", _fromUtf8(msg))
            #msgBox.exec_()

    def stopped(self):
        super(IntersectionDialog, self).stopped()
        self.cancelButton.show()

class ExecDialog(ProgressDialog):
    """
    ProgressDialog extented by an executable external process
    """
    def __init__(self, parent=None, auto_close=False):
        super(ExecDialog, self).__init__(parent=parent, auto_close=auto_close)

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        self.auto_close = auto_close

        # Just to prevent accidentally running multiple times
        # Disable the button when process starts, and enable it when it finishes
        self.process.started.connect(self.running)
        self.process.finished.connect(self.finished)

    def running(self):
        self.cancelButton.clicked.connect(self.kill)
        super(ExecDialog, self).running()

    def stopped(self):
        self.cancelButton.clicked.disconnect(self.kill)
        super(ExecDialog, self).stopped()

    def finished(self):
        if self.process.exitCode() == QtCore.QProcess.NormalExit:
            self.progress_bar.setValue(100)
            self.progress_bar.setStyleSheet(FINISHED_STYLE)
        else:
            self.progress_bar.setStyleSheet(ABORTED_STYLE)
        self.stopped()

    def kill(self):
        self.progress_bar.setStyleSheet(ABORTED_STYLE)
        self.process.kill()
        self.log_edit.insertHtml('<b> Vorgang abgebrochen </b> <br>')
        self.log_edit.moveCursor(QtGui.QTextCursor.End)


class ExecUploadShape(ExecDialog):
    def __init__(self, db_connection, schema, name, shapefile, upload_function,
                 srid=None, parent=None, on_finish=None, on_success=None, auto_close=False):
        super(ExecUploadShape, self).__init__(parent=parent, auto_close=auto_close)
        self.schema = schema
        self.name = name
        self.shapefile = shapefile
        self.db_connection = db_connection
        self.srid = srid
        self.conversion = QtCore.QProcess(self)
        self.on_finish = on_finish
        self.on_success = on_success
        self.upload_function = upload_function

        self.conversion.started.connect(self.running)
        self.conversion.finished.connect(self.conversion_finished)
        self.process.started.disconnect(self.running)

        # start process directly (simulate click on start)
        self.startButton.clicked.emit(True)
        # in fact in this case we don't need a start button at all
        self.startButton.hide()

    # overwrite: we have to process in execupload (conversion before process)
    def kill(self):
        self.progress_bar.setStyleSheet(ABORTED_STYLE)
        self.process.kill()

    def conversion_finished(self):
        if self.conversion.exitCode() == QtCore.QProcess.Crashed:
            self.progress_bar.setStyleSheet(ABORTED_STYLE)
            self.stopped()

    def run(self):
        self.upload_function(
            self.schema, self.name, self.shapefile,
            self.process, self.conversion, srid=self.srid,
            on_progress=self.show_status,
            on_finish=self.on_finish,
            on_success=self.on_success)


class ExecDownloadResultsShape(ExecDialog):
    def __init__(self, db_connection, columns, filename, parent=None, auto_close=False):
        super(ExecDownloadResultsShape, self).__init__(parent=parent, auto_close=auto_close)
        self.filename = filename
        self.db_connection = db_connection
        self.columns = columns

        # start process directly (simulate click on start)
        self.startButton.clicked.emit(True)
        # in fact in this case we don't need a start button at all
        self.startButton.hide()

    def run(self):
        self.db_connection.results_to_shape(
            self.columns, self.process, self.filename,
            on_progress=self.show_status)

class ExecDownloadTableShape(ExecDialog):
    def __init__(self, db_connection, schema, table, filename, columns=None, parent=None, auto_close=False):
        super(ExecDownloadTableShape, self).__init__(parent=parent, auto_close=auto_close)
        self.filename = filename
        self.db_connection = db_connection
        self.schema = schema
        self.table = table
        self.columns = columns

        # start process directly (simulate click on start)
        self.startButton.clicked.emit(True)
        # in fact in this case we don't need a start button at all
        self.startButton.hide()

    def run(self):
        self.db_connection.db_table_to_shape_file(
            self.schema, self.table, self.process, self.filename,
            columns=self.columns, on_progress=self.show_status)


class DownloadTablesDialog(QtGui.QDialog, Ui_DownloadDataDialog):
    def __init__(self, db_conn, parent=None):
        super(DownloadTablesDialog, self).__init__(parent)
        self.setupUi(self)
        self.download_button.clicked.connect(self.download)
        self.cancel_button.clicked.connect(self.close)
        self.db_conn = db_conn

        header = QtGui.QTreeWidgetItem(["Kategorie","Beschreibung"])
        self.tables_to_download_tree.setHeaderItem(header)
        self.tables_to_download_tree.itemClicked.connect(check_status)

        self.select_dir_button.clicked.connect(
            lambda: set_directory(self, self.dir_edit))

#        self.tables_to_download_tree.clear()
        tables_to_download = db_conn.get_tables_to_download()
        self.schemata = {}
        prev_cat = None
        for id, name, schema, tablename, category in tables_to_download:
            self.schemata[tablename] = schema
            if prev_cat != category:
                cat_item = QtGui.QTreeWidgetItem(self.tables_to_download_tree, [_fromUtf8(category)])
                cat_item.setCheckState(0,QtCore.Qt.Unchecked)
                cat_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                prev_cat = category

            col_item = QtGui.QTreeWidgetItem(cat_item, [_fromUtf8(tablename)])
            col_item.setCheckState(0,QtCore.Qt.Unchecked)
            col_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            col_item.setText(1, _fromUtf8(name))

        self.tables_to_download_tree.resizeColumnToContents(0)

        self.show()

    def download(self):
        directory = self.dir_edit.text()
        if not directory:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warnung!",
                                       _fromUtf8('Sie müssen ein Zielverzeichnis wählen!'))
            msgBox.exec_()
            return

        selected_tables = get_selected(self.tables_to_download_tree)

        for table in selected_tables:
            table = str(table)
            filename = os.path.join(str(directory), table + '.csv')
            schema = self.schemata[table]
            diag = ExecDownloadTableShape(self.db_conn, schema, table, filename, parent=self, auto_close=True)
            diag.exec_()

        self.close()