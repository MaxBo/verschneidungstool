# -*- coding: utf-8 -*-
import psycopg2
from verschneidungstool.connection import Connection
from verschneidungstool.config import Config
from PyQt5 import QtCore
import tempfile, os, shutil, re
import csv
import xlwt

config = Config()


class DBConnection(object):
    def __init__(self, login):
        self.login = login
        self.colums_available = None

    def fetch(self, sql):
        with Connection(login=self.login) as conn:
            self.conn = conn
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows

    def copy_expert(self, sql, fileobject):
        with Connection(login=self.login) as conn:
            self.conn = conn
            cursor = self.conn.cursor()
            cursor.copy_expert(sql, fileobject)

    def execute(self, sql):
        with Connection(login=self.login) as conn:
            self.conn = conn
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
            except psycopg2.ProgrammingError as e:
                raise psycopg2.ProgrammingError(
                    os.linesep.join((sql, str(e))))
            conn.commit()

    def get_areas_available(self):
        sql = """
        SELECT id, area_name, schema, table_name, can_be_deleted, default_stops,
        results_schema, results_table, check_last_calculation
        FROM meta.areas_available
        ORDER BY id
        """
        return self.fetch(sql)

    def get_stations_available(self):
        sql = """
        SELECT id, name, schema, can_be_deleted
        FROM meta.haltestellen_available
        ORDER BY id
        """
        return self.fetch(sql)

    def get_years_available(self):
        sql = """
        SELECT year
        FROM meta.years_available
        ORDER BY year
        """
        return self.fetch(sql)

    def get_tables_to_download(self):
        sql = """
        SELECT id, name, schema, tablename, category
        FROM meta.tables_to_download
        ORDER BY category
        """
        return self.fetch(sql)

    def get_structure_available(self, year):
        if not self.colums_available:
            sql_col_avail = """
            SELECT *
            FROM meta.columns_available
            ORDER BY table_type, id
            """
            col_avail = self.fetch(sql_col_avail)
            self.colums_available = {}
            for record in col_avail:
                if record.table_type not in self.colums_available:
                    self.colums_available[record.table_type] = []
                self.colums_available[record.table_type].append({
                    'name': record.column, 'description': record.description})

        sql_cat = """
        SELECT tc.name
        FROM meta.table_categories AS tc,
        meta.column_definitions AS cd
        WHERE tc.name = cd.table_category
        AND cd.from_year <= {year}
        AND cd.to_year >= {year}
        ORDER BY id
        """
        sql_cat = sql_cat.format(year=year)
        categories = self.fetch(sql_cat)
        structure = {}

        for record in categories:
            structure[record.name] = self.colums_available[record.name]
        return structure

    def get_schemata_available(self):
        sql = """
        SELECT name
        FROM meta.schemata_available
        """
        return self.fetch(sql)

    def drop_area(self, id, table, schema):

        last = self.get_last_calculated()
        if schema == last[0].schema and table == last[0].table_name:
            return False,
        ('{schema}.{table} kann nicht gelöscht werden,\n'
         .format(schema=schema, table=table) +
         'da die letzte Verschneidung mit dieser Aggregation erfolgte. \n\n'
         'Bitte führen Sie zunächst eine Verschneidung mit einer\n'
         'anderen Aggregationsstufe durch, bevor Sie diese löschen.')
        # remove row from available schemata
        sql_remove = """
        DELETE FROM meta.areas_available
        WHERE id = {id}
        """
        # drop table
        sql_drop = """
        Drop TABLE IF EXISTS {schema}.{table}
        """
        try:
            self.execute(sql_remove.format(id=id))
            self.execute(sql_drop.format(schema=schema, table=table))
            return True, 'Löschen von {schema}.{table} erfolgreich'.format(
                schema=schema, table=table)
        except:
            return False, ('Ein datenbankinterner Fehler ist beim '
                           'Löschen aufgetreten')

    def drop_stations(self, id, table, schema):

        sql_check = """
        SELECT area_name FROM meta.areas_available WHERE default_stops = {hst_id}
        """

        check = self.fetch(sql_check.format(hst_id=id))
        if len(check) > 0:
            msg = ('{schema}.{table} kann nicht gelöscht werden, '
                   'da die Aggregationsstufen \n'
                   .format(schema=schema, table=table))
            for c in check:
                msg += ' - ' + c.area_name + '\n'
            msg += 'darauf verweisen!'
            return False, msg

        last = self.get_last_calculated()
        if schema == last[0].hst_schema and table == last[0].hst_name:
            return False, ('{schema}.{table} kann nicht gelöscht werden,\n'
                           .format(schema=schema, table=table) +
                           'da die letzte Verschneidung mit diesen'
                           'Haltestellen erfolgte. \n\n'
                           'Bitte führen Sie zunächst eine Verschneidung mit \n'
                           'anderen Haltestellen durch, bevor Sie'
                           'diese löschen.')
        # remove row from available schemata
        sql_remove = """
        DELETE FROM meta.haltestellen_available
        WHERE id = {id}
        """
        # drop table
        sql_drop = """
        Drop TABLE IF EXISTS {schema}.{table}
        """
        try:
            self.execute(sql_remove.format(id=id))
            self.execute(sql_drop.format(table=table, schema=schema))
            return (True, 'Löschen von {schema}.{table} erfolgreich'
                    .format(schema=schema, table=table))
        except:
            return (False, 'Ein datenbankinterner Fehler ist beim '
                    'Löschen aufgetreten')

    def get_projections_available(self):
        sql = """
        SELECT *
        FROM meta.projections_available
        ORDER BY srid
        """
        return self.fetch(sql)

    def add_projection(self, srid, description):
        sql = """
        INSERT INTO meta.projections_available (srid, description)
        VALUES ('{srid}','{description}');
        """
        return self.execute(sql.format(srid=srid, description=description))

    def get_srid(self, projection_data):
        sql = """
        SELECT prjtxt2epsg('{}')
        """
        return self.fetch(sql.format(projection_data))

    def get_spatial_ref(self, srid):
        sql = """
        SELECT srtext
        FROM spatial_ref_sys
        WHERE srid = {}
        """
        return self.fetch(sql.format(srid))

    def get_column_names(self, schema, table):
        sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table}'
        """
        return self.fetch(sql.format(schema=schema, table=table))

    def get_pkey(self, schema, table):
        '''
        get the current primary key of given table
        '''
        sql = """
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{schema}.{table}'::regclass
        AND    i.indisprimary;
        """
        ret = [a.attname for a in self.fetch(sql.format(
            schema=schema, table=table))]
        return ret

    def set_zone(self, schema, table, hst_id, zone_id_column=None,
                 zone_name_column=''):
        '''
        set the columns with the zone-id, zone-name and default_stops for the given
        area table makes an entry in the areas_available table, that this column is
        preferred as pkey
        returns True if successful
        returns False if not (e.g. column isn't unique, table doesn't exist)
        '''

        # zone-id
        sql_unique = """
        ALTER TABLE {schema}.{table}
        ADD UNIQUE ({column})
        """
        try:
            pkey = self.get_pkey(schema, table)
        except Exception as e:
            return False, e
        if len(pkey) != 1:
            return (False, 'Kein eindeutiger primary key in hochgeladener'
                    'Tabelle vorhanden!')
        pkey = pkey[0]
        if not zone_id_column:
            zone_id_column = pkey
        if not zone_name_column:
            zone_name_column = zone_id_column
        else:
            # set custom zone-id column to unique to check if values are unique
            try:
                self.execute(sql_unique.format(schema=schema,
                                               table=table,
                                               column=zone_id_column))
            # catches all exception (e.g. if table doesn't exist)
            except Exception as e:
                return False, e

        sql_update = """
        UPDATE meta.areas_available
        SET pkey='{pkey}', zone_id='{zone_id}', zone_name='{zone_name}',
        default_stops={hst_id}
        WHERE schema='{schema}'
        AND table_name='{table}'
        """
        # update the meta table
        self.execute(sql_update.format(pkey=pkey, zone_id=zone_id_column,
                                       zone_name=zone_name_column,
                                       hst_id=hst_id,
                                       schema=schema, table=table))
        return True, ''

    def upload_shape(self, schema, name, shapefile, process, conversion_process,
                 on_progress=None, srid=None, on_exit=None, encoding='UTF-8'):
        '''
        upload a shapefile to the database, monitor the progress

        @param schema - the schema the table will be created in
        @param name - the name the area (= the table) gets
        @param shapefile - the path to the shapefile to upload
        @param process - QtCore.QProcess, process provided to upload shape into db
        @param conversion - QtCore.QProcess, process provided to convert file
        @param on_progress - optional, method expecting a string as a parameter
        and an optional progress value (from 0 to 100)
        @param on_exit - optional, additional callback, called when process is done,
        expects exit-code and -status as params
        @param projection - optional, srid of the projection
        @param encoding - optional, encoding of the shapefile
        '''
        psql_path = config.settings['env']['psql_path']
        shp2pgsql_path = config.settings['env']['shp2pgsql_path']

        if not os.path.exists(psql_path):
            psql_path = os.path.join(os.path.dirname(__file__),
                                     psql_path)
        if not os.path.exists(psql_path):
            on_progress(u'<b>Die angegebene <i>psql_path.exe</i> wurde '
                        'nicht gefunden. </br> Bitte prüfen Sie die '
                        'Einstellungen!</b>')
            return

        if not os.path.exists(shp2pgsql_path):
            shp2pgsql_path = os.path.join(os.path.dirname(__file__),
                                          shp2pgsql_path)
        if not os.path.exists(shp2pgsql_path):
            on_progress(u'<b>Die angegebene <i>shp2pgsql_path.exe</i> wurde '
                        'nicht gefunden. </br> Bitte prüfen Sie die '
                        'Einstellungen!</b>')
            return

        options = '-c -g geom -I'
        self.on_progress = on_progress
        target_srid = config.settings['db_config']['srid']
        if srid:
            options += ' -s {sourcesrid}:{target_srid}'.format(
                sourcesrid=srid, target_srid=target_srid)
        options += ' -W {}'.format(encoding)
        #put tmp file in folder where this script is located
        tmp_dir = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_dir, 'temp.sql')
        shp2pgsql_cmd = (u'"{executable}" {options} "{input_file}" '
                         '{schema}.{table}"'.format(
                             executable=shp2pgsql_path, options=options,
                             input_file=shapefile, schema=schema, table=name)
                         )

        def finished(exit_code, exit_status):
            on_exit(exit_code, exit_status)
            shutil.rmtree(tmp_dir)

        # call callback with standard error and output
        def progress():
            if process.state() != QtCore.QProcess.NotRunning:
                out = bytearray(process.readAllStandardOutput())
                err = bytearray(process.readAllStandardError())
                if len(out) > 0: on_progress(out.decode('utf-8'))
                if len(err) > 0: on_progress(err.decode('utf-8'))

            if conversion_process.state() != QtCore.QProcess.NotRunning:
                self.on_progress(str(conversion_process.readAllStandardError()))

        if self.on_progress:
            # QProcess emits `readyRead` when there is data to be read
            conversion_process.readyReadStandardError.connect(progress)
            process.readyReadStandardOutput.connect(progress)
            process.readyReadStandardError.connect(progress)

        def upload_to_db(exit_code, exit_status):
            if(exit_code != 0):
                if(self.on_progress):
                    self.on_progress('<b>Konvertierung nicht '
                                     'erfolgreich </b><br>')
                return
            if self.on_progress:
                self.on_progress('<b>Konvertierung erfolgreich. '
                                 'Starte Upload... </b><br>', 50)

            db_config = config.settings['db_config']
            # you can't pass a password to the command-line psql.exe
            # -> set environment variable instead
            sys_env = QtCore.QProcessEnvironment.systemEnvironment()
            sys_env.insert("PGPASSWORD", db_config['password'])
            process.setProcessEnvironment(sys_env)

            psql_cmd = (u'"{executable}" -d {database} -a -h {host} -p {port}'
                        ' -U {user} -w -f "{input_file}"'.format(
                            executable=psql_path, database=db_config['db_name'],
                            host=db_config['host'], port=db_config['port'],
                            user=db_config['username'], input_file=tmp_file))

            process.finished.connect(finished)
            process.start(psql_cmd)

        conversion_process.finished.connect(upload_to_db)

        def read_sql_code():
            txt = conversion_process.readAllStandardOutput()
            with open(tmp_file, 'ab') as openfile:
                openfile.write(txt)

        conversion_process.readyReadStandardOutput.connect(read_sql_code)
        conversion_process.start(shp2pgsql_cmd)

    def add_area(self, schema, name, shapefile, process, conversion_process,
                 on_progress=None, srid=None, on_finish=None, on_success=None,
                 encoding='UTF-8'):
        '''
        add an aggregation area based on a given shapefile to the database, monitor
        the progress

        @param schema - the schema the table will be created in
        @param name - the name the area (= the table) gets
        @param shapefile - the path to the shapefile to upload
        @param process - QtCore.QProcess, process provided to upload shape into db
        @param conversion - QtCore.QProcess, process provided to convert file
        @param on_progress - optional, method expecting a string as a parameter and
        an optional progress value (from 0 to 100)
        @param on_finish - optional, additional callback, called when run is finished
        @param on_success - optional, additional callback, called when run was
        successful
        @param projection - optional, srid of the projection
        '''

        self.on_progress = on_progress

        def on_exit(exit_code, exit_status):
            if exit_code == 0:
                # add new area to areas_available
                sql = """
                INSERT INTO meta.areas_available (area_name, schema, table_name, can_be_deleted)
                VALUES ('{area_name}','{schema}', '{table}', 'TRUE');
                """
                sql_alter = """
                ALTER TABLE {schema}.{table}
                OWNER TO verkehr;
                """
                self.execute(sql.format(
                    area_name=name, schema=schema, table=name))
                self.execute(sql_alter.format(schema=schema, table=name))
                if self.on_progress:
                    self.on_progress('<b>Upload erfolgreich</b><br>')
                self.on_progress = None
            if on_finish:
                on_finish()
            # on_success hast to be called after on_finish (this one is called
            # on error as well)
            if exit_code == 0 and on_success:
                on_success()

        self.upload_shape(schema, name, shapefile, process, conversion_process,
                          on_progress=on_progress, srid=srid, on_exit=on_exit,
                          encoding=encoding)

    def add_stations(self, schema, name, shapefile, process, conversion_process,
                 on_progress=None, srid=None, on_finish=None, on_success=None,
                 encoding='UTF-8'):
        '''
        add stations based on a given shapefile to the database, monitor the progress

        @param schema - the schema the table will be created in
        @param name - the name the area (= the table) gets
        @param shapefile - the path to the shapefile to upload
        @param process - QtCore.QProcess, process provided to upload shape into db
        @param conversion - QtCore.QProcess, process provided to convert file
        @param on_progress - optional, method expecting a string as a parameter
        and an optional progress value (from 0 to 100)
        @param on_finish - optional, additional callback, called when run
        is finished
        @param on_success - optional, additional callback, called when run was
        successful
        @param projection - optional, srid of the projection
        '''

        self.on_progress = on_progress

        def on_exit(exit_code, exit_status):
            if exit_code == 0:
                # add new area to areas_available
                sql = """
                INSERT INTO meta.haltestellen_available (name, schema, can_be_deleted)
                VALUES ('{name}','{schema}', 'TRUE');
                """
                sql_alter = """
                ALTER TABLE {schema}.{table}
                OWNER TO verkehr;
                """
                self.execute(sql.format(name=name, schema=schema))
                self.execute(sql_alter.format(schema=schema, table=name))
                if self.on_progress:
                    self.on_progress('<b>Upload erfolgreich</b><br>')
                self.on_progress = None
            if on_finish:
                on_finish()
            # on_success hast to be called after on_finish (this one is
            # called on error as well)
            if exit_code == 0 and on_success:
                on_success()

        self.upload_shape(schema, name, shapefile, process, conversion_process,
                          on_progress=on_progress, srid=srid, on_exit=on_exit,
                          encoding=encoding)

    def new_intersection(self, schema, table):
        # set functions to scope of following class
        fetch = self.fetch
        execute = self.execute

        class Intersection(QtCore.QThread):
            progress = QtCore.pyqtSignal(str, int)
            error = QtCore.pyqtSignal(str)
            def __init__(self):
                QtCore.QThread.__init__(self)

            def run(self):

                sql_pkey = """
                SELECT pkey, zone_name, zone_id
                FROM meta.areas_available
                WHERE schema='{schema}'
                AND table_name='{table}';
                """

                sql_queries = """
                SELECT * FROM meta.queries ORDER BY id;
                """

                try:
                    row = fetch(sql_pkey.format(schema=schema, table=table))[0]
                except IndexError:
                    msg = ('Tabelle {schema}.{table}.\nnicht in der Datenbank '
                           'vorhanden.'.format(schema=schema, table=table))
                    self.error.emit(msg)
                    return

                pkey = row.pkey
                zone_name = row.zone_name
                zone_id = row.zone_id

                queries = fetch(sql_queries)

                if (not pkey) or (not zone_id):
                    msg = ('Fehlerhafter Eintrag für {schema}.{table}.\nEs '
                           'ist keine zone_id oder kein primary key angegeben.'
                           .format(schema=schema, table=table))
                    self.error.emit(msg)
                    return

                self.progress.emit('Starte Verschneidung...', 0)

                if zone_name is None or zone_name == '':
                    name_str = "''"
                else:
                    name_str = 't."{zone_name}"'.format(zone_name=zone_name)
                sql_prep = """
                INSERT INTO meta.scenario (area_id, start_time, end_time, started, finished)
                SELECT a.id, clock_timestamp(), NULL,  True, False
                FROM meta.areas_available AS a
                WHERE a.schema = '{schema}' AND a.table_name = '{table}';
                CREATE OR REPLACE VIEW verkehrszellen.view_vz_aktuell_3044 (id, geom, zone_name) AS
                SELECT
                t."{pkey}"::integer AS id,
                st_multi(st_transform(t.geom, 3044))::geometry(MULTIPOLYGON, 3044) AS geom,
                {name_str}::text AS zone_name

                FROM {schema}.{table} AS t;
                """
                try:
                    execute(sql_prep.format(pkey=zone_id, schema=schema,
                                            table=table,
                                            name_str=name_str))
                except psycopg2.ProgrammingError as e:
                    self.error.emit(str(e))
                    return

                self.add_pnt_column_if_exists(zone_id, name_str)

                weight_sum = sum(q.weight for q in queries)
                progress = 0

                for query in queries:
                    self.progress.emit(query.message, progress)
                    try:
                        execute(query.command)
                    except psycopg2.Error as e:
                        self.error.emit(os.linesep.join((
                            query.command, str(e))))
                        return
                    progress += (query.weight / weight_sum) * 100


                self.progress.emit('Nachbereitungen laufen...', progress)

                sql_post = """
                UPDATE meta.scenario AS sc SET end_time=clock_timestamp(), started=False, finished=True
                FROM meta.areas_available AS a, meta.last_area_calculated AS l
                WHERE a.schema='{schema}' AND a.table_name='{table}'
                AND l.id = sc.id;
                """
                execute(sql_post.format(schema=schema, table=table))

                self.progress.emit('Verschneidung beendet!', 100)

                return

            def add_pnt_column_if_exists(self, zone_id, name_str):
                # add point column, if exists
                col_pnt = 'pnt'
                sql_col_exists = '''
                            SELECT EXISTS (SELECT 1
                            FROM information_schema.columns
                            WHERE table_schema='{schema}'
                            AND table_name='{table}'
                            AND column_name='{col}');
                            '''
                col_exists = fetch(sql_col_exists.format(schema=schema,
                                                         table=table,
                                                         col=col_pnt))
                if col_exists[0][0]:
                    pnt_col_def = 't.{}::geometry(POINT)'.format(col_pnt)
                else:
                    pnt_col_def = 'st_pointonsurface(t.geom)::geometry(POINT)'

                sql_pnt = """
                CREATE OR REPLACE VIEW verkehrszellen.view_vz_aktuell_pnt (id, pnt, zone_name) AS
                SELECT
                t."{pkey}"::integer AS id,
                {pnt_col_def} AS pnt,
                {name_str}::text AS zone_name

                FROM {schema}.{table} AS t;"""
                execute(sql_pnt.format(pkey=zone_id,
                                       schema=schema, table=table,
                                       name_str=name_str,
                                       pnt_col_def=pnt_col_def))

        thread = Intersection()
        return thread

    def set_current_year(self, year):
        sql = """
        UPDATE meta.current_year
        SET jahr='{year}'
        """
        self.execute(sql.format(year=year))

    def set_current_stations(self, table, schema):
        sql = """
        UPDATE haltestellen.hst_selected
        SET name='{name}', schema='{schema}'
        """
        self.execute(sql.format(name=table, schema=schema))

    def get_last_calculated(self):
        sql = """
        SELECT *
        FROM meta.last_area_calculated
        """
        return self.fetch(sql)

    def force_reset_calc(self):
        '''
        resets the database entry for locking calculations to be able to start
        new last row is identified by max id
        warning: if a calculation is still running, new calculation may result
        in errors
        '''
        sql = """
        UPDATE meta.scenario
        SET finished = true
        WHERE id = (SELECT max(id) FROM meta.scenario )
        """
        self.execute(sql)


    # empty column array selects all columns (*)
    def db_table_to_csv_file(self, schema, table, filename, columns=None):
        sql = '''
        COPY (SELECT {columns}
        FROM {schema}.{table}) TO STDOUT WITH CSV HEADER
        '''
        if columns and len(columns) > 0:
            columns = ['"{}"'.format(c) for c in columns]
            columns = ','.join(columns)
        else:
            columns = '*'

        with open(filename, 'w') as fileobject:
            self.copy_expert(sql.format(
                columns=columns, table=table, schema=schema), fileobject)

    def results_to_csv(self, schema, table, columns, filename):
        columns = ['vz_id', 'zone_name'] + columns
        self.db_table_to_csv_file(schema, table, filename, columns=columns)

    def results_to_excel(self, schema, table, columns, filename):
        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, 'temp.csv')
        self.results_to_csv(schema, table, columns, tmp_filename)

        with open(tmp_filename, 'r') as f:
            csvreader = csv.reader((f), delimiter=",")
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("Sheet 1")
            for r, row in enumerate(csvreader):
                for c, value in enumerate(row):
                    try:
                        val = float(value)
                    except ValueError:
                        val = value
                    sheet.write(r, c, val)
            wbk.save(filename)

    def db_table_to_shape_file(self, schema, table, process, filename,
                               columns=None,  on_progress=None,
                               srid=None, on_finish=None):
        pgsql2shp_path = config.settings['env']['pgsql2shp_path']
        db_config = config.settings['db_config']

        if not os.path.exists(pgsql2shp_path):
            pgsql2shp_path = os.path.join(os.path.dirname(__file__),
                                          pgsql2shp_path)

        if not os.path.exists(pgsql2shp_path):
            on_progress(u'<b>Die angegebene <i>pgsql2shp.exe</i> wurde nicht '
                        'gefunden. </br> Bitte prüfen Sie die Einstellungen!'
                        '</b>')
            return

        if columns and len(columns) > 0:
            columns = ['"\""{}"\""'.format(c) for c in columns]
            columns = ','.join(columns)
        else:
            columns = '*'

        sql = 'SELECT {columns} FROM {schema}.{table}'

        pgsql2shp_cmd = (u'"{executable}" -f "{filename}" -h {host} -p {port} '
                         '-u {user} -P {password} {database} "{sql}"'.format(
                             executable=pgsql2shp_path,
                             filename=filename,
                             database=db_config['db_name'],
                             host=db_config['host'],
                             port=db_config['port'],
                             user=db_config['username'],
                             password=db_config['password'],
                             sql=sql.format(columns=columns,
                                            schema=schema, table=table)
        ))

        # call callback with standard error and output
        def progress():
            out = bytearray(process.readAllStandardOutput())
            err = bytearray(process.readAllStandardError())
            if len(out) > 0: on_progress(out.decode('utf-8'))
            if len(err) > 0: on_progress(err.decode('utf-8'))

        if on_progress:
            process.readyReadStandardOutput.connect(progress)
            process.readyReadStandardError.connect(progress)

        on_progress('Konvertiere {schema}.{table} in {filename}'.format(
            schema=schema, table=table, filename=filename))
        process.start(pgsql2shp_cmd)


    def results_to_shape(self, schema, table, columns, process, filename,
                         on_progress=None, srid=None, on_finish=None):
        columns = ['vz_id', 'zone_name', 'geom'] + columns
        self.db_table_to_shape_file(schema, table, process, filename,
                                   columns=columns, on_progress=on_progress,
                                   srid=srid, on_finish=on_finish)


def parse_projection_file(filename):
    '''
    parse and return the complete data, projcs and geogcs description out of a
    given .prj file
    '''
    with open(filename) as f:
        data = f.read()
        projcs, geogcs = parse_projection_data(data)

    return data, projcs, geogcs

def parse_projection_data(data):
    '''
    parse and return the projcs and geogcs description out of a projection-string
    '''
    projcs_pattern = 'PROJCS\["(.*?)",'
    projcs_matches = re.findall(projcs_pattern, data)
    geogcs_pattern = 'GEOGCS\["(.*?)",'
    geogcs_matches = re.findall(geogcs_pattern, data)

    projcs = projcs_matches[0] if len(projcs_matches) > 0 else None
    geogcs = geogcs_matches[0] if len(geogcs_matches) > 0 else None

    return projcs, geogcs
