# -*- coding: utf-8 -*-
import psycopg2
from extractiontools.connection import Connection
from gui_hannover.config import Config
from PyQt4 import QtCore
import tempfile, os, shutil, re
import unicodecsv as csv
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
            cursor.execute(sql)
            conn.commit()

    def get_areas_available(self):
        sql = """
        SELECT id, area_name, schema, table_name, can_be_deleted
        FROM meta.areas_available
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
                if not (self.colums_available.has_key(record.table_type)):
                    self.colums_available[record.table_type] = []
                self.colums_available[record.table_type].append(record.column)

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
            return True
        except:
            return False

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

    '''
    get the current primary key of given table
    '''
    def get_pkey(self, schema, table):
        sql = """
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{schema}.{table}'::regclass
        AND    i.indisprimary;
        """
        ret = [a.attname for a in self.fetch(sql.format(schema=schema, table=table))]
        return ret

    '''
    set the columns with the zone-id and zone-name for the given area table
    makes an entry in the areas_available table, that this column is preferred as pkey
    returns True if successful
    returns False if not (e.g. column isn't unique, table doesn't exist)
    '''
    def set_zone(self, schema, table, zone_id_column=None, zone_name_column=''):

        # zone-id
        sql_unique = """
        ALTER TABLE {schema}.{table}
        ADD UNIQUE ({column})
        """

        pkey = self.get_pkey(schema, table)
        if len(pkey) != 1:
            return False, 'Kein eindeutiger primary key in hochgeladener Tabelle vorhanden!'
        pkey = pkey[0]
        if not zone_id_column:
            zone_id_column = pkey
        else:
            # set custom zone-id column to unique to check if values are unique
            try:
                self.execute(sql_unique.format(schema=schema, table=table, column=zone_id_column))
            # catches all exception (e.g. if table doesn't exist)
            except Exception as e:
                return False, e

        sql_update = """
        UPDATE meta.areas_available
        SET pkey='{pkey}', zone_id='{zone_id}', zone_name='{zone_name}'
        WHERE schema='{schema}'
        AND table_name='{table}'
        """
        # update the meta table
        self.execute(sql_update.format(pkey=pkey, zone_id=zone_id_column,
                                       zone_name=zone_name_column,
                                       schema=schema, table=table))
        return True, ''

    '''
    add an aggregation area based on a given shapefile to the database, monitor the progress

    @param schema - the schema the table will be created in
    @param name - the name the area (= the table) gets
    @param shapefile - the path to the shapefile to upload
    @param process - QtCore.QProcess, process provided to upload shape into db
    @param conversion - QtCore.QProcess, process provided to convert file
    @param on_progress - optional, method expecting a string as a parameter and an optional progress value (from 0 to 100)
    @param on_finish - optional, additional callback, called when run is finished
    @param on_success - optional, additional callback, called when run was successful
    @param projection - optional, srid of the projection
    '''
    def add_area(self, schema, name, shapefile, process, conversion_process,
                 on_progress=None, srid=None, on_finish=None, on_success=None):
        psql_path = config.settings['env']['psql_path']
        shp2pgsql_path = config.settings['env']['shp2pgsql_path']
        options = '-c -g geom -I'
        self.on_progress = on_progress
        target_srid = config.settings['db_config']['srid']
        if srid:
            options += ' -s {sourcesrid}:{target_srid}'.format(sourcesrid=srid,
                                                               target_srid=target_srid)
        #put tmp file in folder where this script is located
        tmp_dir = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_dir, 'temp.sql')
        shp2pgsql_cmd = '"{executable}" {options} "{input_file}" {schema}.{table}"'.format(
            executable=shp2pgsql_path, options=options, input_file=shapefile, schema=schema, table=name)
        print shp2pgsql_cmd

        # call callback with standard error and output
        def progress():
            if process.state() != QtCore.QProcess.NotRunning:
                out = str(process.readAllStandardOutput())
                err = str(process.readAllStandardError())
                if len(out) > 0: self.on_progress(out)
                if len(err) > 0: self.on_progress(err)
            if conversion_process.state() != QtCore.QProcess.NotRunning:
                self.on_progress(str(conversion_process.readAllStandardError()))

        if self.on_progress:
            # QProcess emits `readyRead` when there is data to be read
            conversion_process.readyReadStandardError.connect(progress)
            process.readyReadStandardOutput.connect(progress)
            process.readyReadStandardError.connect(progress)

        def finished(exit_code, exit_status):
            shutil.rmtree(tmp_dir)
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
                self.execute(sql.format(area_name=name, schema=schema, table=name))
                self.execute(sql_alter.format(schema=schema, table=name))
                if self.on_progress:
                    self.on_progress('<b>Upload erfolgreich</b><br>')
                self.on_progress = None
            if on_finish:
                on_finish()
            # on_success hast to be called after on_finish (this one is called on error as well)
            if exit_code == 0 and on_success:
                on_success()

        def upload_to_db(exit_code, exit_status):
            if(exit_code != 0):
                if(self.on_progress):
                    self.on_progress('<b>Konvertierung nicht erfolgreich </b><br>')
                return
            if self.on_progress:
                self.on_progress('<b>Konvertierung erfolgreich. Starte Upload... </b><br>', 50)

            db_config = config.settings['db_config']
            # you can't pass a password to the command-line psql.exe -> set environment variable instead
            sys_env = QtCore.QProcessEnvironment.systemEnvironment()
            sys_env.insert("PGPASSWORD", db_config['password'])
            process.setProcessEnvironment(sys_env)

            psql_cmd = '"{executable}" -d {database} -a -h {host} -p {port} -U {user} -w -f "{input_file}"'.format(
                executable=psql_path, database=db_config['db_name'],
                host=db_config['host'], port=db_config['port'],
                user=db_config['username'], input_file=tmp_file)
            process.finished.connect(finished)
            process.start(psql_cmd)

        conversion_process.finished.connect(upload_to_db)

        def read_sql_code():
            txt = conversion_process.readAllStandardOutput()
            with open(tmp_file, 'ab') as openfile:
                openfile.write(txt)

        conversion_process.readyReadStandardOutput.connect(read_sql_code)
        conversion_process.start(shp2pgsql_cmd)

    def new_intersection(self, schema, table):
        # set functions to scope of following class
        fetch = self.fetch
        execute = self.execute

        class Intersection(QtCore.QThread):
            def __init__(self):
                QtCore.QThread.__init__(self)

            def run(self):

                sql_pkey = """
                SELECT pkey, zone_name
                FROM meta.areas_available
                WHERE schema='{schema}'
                AND table_name='{table}'
                """

                row = fetch(sql_pkey.format(schema=schema, table=table))[0]
                pkey = row.pkey
                zone_name = row.zone_name

                progress_signal = 'progress(QString, QVariant)'
                signal = QtCore.SIGNAL(progress_signal)
                if not pkey:
                    msg = 'Fehlerhafter Eintrag für {schema}.{table}.\nEs ist kein primary key angegeben.'.format(schema=schema, table=table)
                    self.emit( signal, msg, 0)
                    return

                self.emit(signal, 'Starte Verschneidung...', 0)

                if zone_name is None or zone_name == '':
                    name_str = "''"
                else:
                    name_str = 't."{zone_name}"'.format(zone_name=zone_name)
                sql_prep = """
                INSERT INTO meta.scenario (area_id, start_time, end_time, started, finished)
                SELECT a.id, clock_timestamp(), NULL,  True, False
                FROM meta.areas_available AS a
                WHERE a.schema = '{schema}' AND a.table_name = '{table}';
                CREATE OR REPLACE VIEW verkehrszellen.view_vz_aktuell (id, geom) AS
                SELECT
                t."{pkey}"::integer AS id,
                t.geom::geometry(GEOMETRY) AS geom,
                {name_str}::text AS zone_name
                FROM {schema}.{table} AS t;"""
                execute(sql_prep.format(pkey=pkey, schema=schema, table=table,
                                        name_str=name_str))

                self.emit(signal,
                          'Verschneide Verkehrszellen mit Prognosebezirken...',
                        5)

                sql_intersect1 = """
                -- Verschneide neue Verkehrszellen  mit Prognosebezirken
                REFRESH MATERIALIZED VIEW verkehrszellen.mview_vz_progbez;
                """
                execute(sql_intersect1)

                self.emit(signal,
                          'Verschneide Verkehrszellen mit Einzugsbereichen Schiene, Gebietstypen und Gewichtungsfaktor-Shapes...',
                        30)

                sql_intersect2 = """
                -- Verschneide mit Einzugsbereichen Schiene, Gebietstypen und Gewichtungsfaktor-Shapes
                REFRESH MATERIALIZED VIEW verkehrszellen.matview_vz_aktuell_gebietstypen;
                """
                execute(sql_intersect2)

                self.emit(signal,
                         'Verschneide Verkehrszellen mit Baubloecken und Gebaeuden...', 45)

                sql_intersect3 = """
-- Verschneide Baubloecke und Gebaeude mit neuen Verkehrszellen
SELECT gc.intersect_vz('raumeinheiten.skh5_baubloecke', 'baubloecke');
SELECT gc.intersect_centroid_vz('einwohner.view_b1_m_all_buildings', 'building_id');
                """
                execute(sql_intersect3)

                self.emit(signal,
                          'Berechne Einwohnerzahl nach Altersklassen in den neuen Verkehrszellen...', 50)

                sql_intersect4 = """
-- berechne Einwohnerzahl nach Altersklassen in den neuen Verkehrszellen fuer das Analysejahr
REFRESH MATERIALIZED VIEW einwohner.view_l_m_vz_ew_alkl_2015;
                """
                execute(sql_intersect4)


                #"""
                #-- setze das aktuelle Jahr
                #UPDATE meta.current_year
                #SET jahr = {year_selected};
                #"""

                self.emit(signal,
                          'Verschneide geplante Baugebiete mit neuen Verkehrszellen...', 65)

                sql_intersect5 = """
-- Verschneide geplante Baugebiete mit neuen Verkehrszellen
SELECT gc.intersect_vz('planungen.planungen_siedlung_region_2015', 'siedlungsfl_id');
SELECT gc.intersect_vz('planungen.planungen_siedlung_lhh_2015', 'gid');
                """
                execute(sql_intersect5)

                self.emit(signal,
                          'Aktualisiere materialisierte Views...', 70)

                sql_intersect6 = """
REFRESH MATERIALIZED VIEW verkehrszellen.mview_vz_progbez;
REFRESH MATERIALIZED VIEW einwohner.view_l_m_vz_ew_alkl_2015;
--REFRESH MATERIALIZED VIEW einwohner.view_l2_m_vz_ew_alkl_prognosejahr;
                """
                execute(sql_intersect6)

                self.emit( signal,
                           'Nachbereitungen laufen...', 98)

                sql_post = """
UPDATE meta.scenario AS sc SET end_time=clock_timestamp(), started=False, finished=True
FROM meta.areas_available AS a, meta.last_area_calculated AS l
WHERE a.schema='{schema}' AND a.table_name='{table}'
AND l.id = sc.id;
                """
                execute(sql_post.format(schema=schema, table=table))

                self.emit(signal,
                          'Verschneidung beendet!', 100)

                return

        thread = Intersection()
        return thread

    def set_current_year(self, year):
        sql = """
        UPDATE meta.current_year
        SET jahr='{year}'
        """
        self.execute(sql.format(year=year))

    def get_last_calculated(self):
        sql = """
        SELECT *
        FROM meta.last_area_calculated
        """
        return self.fetch(sql)

    def results_to_csv(self, columns, filename):
        sql = '''
        COPY (SELECT vz_id, zone_name {columns}
        FROM strukturdaten.results) TO STDOUT WITH CSV HEADER
        '''
        if columns and len(columns) > 0:
            columns = ['"{}"'.format(c) for c in columns]
            columns = ',' + ','.join(columns)
        else:
            columns = ''

        with open(filename, 'w') as fileobject:
            self.copy_expert(sql.format(columns=columns), fileobject)

    def results_to_excel(self, columns, filename):
        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, 'temp.csv')
        self.results_to_csv(columns, tmp_filename)

        with open(tmp_filename, 'rb') as f:
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

    def results_to_shape(self, columns, process, filename,
                         on_progress=None, srid=None, on_finish=None):
        psql_path = config.settings['env']['psql_path']
        pgsql2shp_path = config.settings['env']['pgsql2shp_path']
        db_config = config.settings['db_config']

        if columns and len(columns) > 0:
            # single quote " needs to be escaped with double quote "" (-> triple quote),
            # because the composed select-query has to be enclosed with double quote "" in the pgsql2shp_cmd as well
            columns = ['"""{}"""'.format(c) for c in columns]
            columns = ',' + ','.join(columns)
        else:
            columns = ''

        sql = 'SELECT vz_id, zone_name, geom {columns} FROM strukturdaten.results'

        pgsql2shp_cmd = '"{executable}" -f "{filename}" -h {host} -p {port} -u {user} -P {password} {database} "{sql}"'.format(
            executable=pgsql2shp_path,
            filename=filename,
            database=db_config['db_name'],
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            sql=sql.format(columns=columns)
        )

        # call callback with standard error and output
        def progress():
            out = str(process.readAllStandardOutput())
            err = str(process.readAllStandardError())
            if len(out) > 0: on_progress(out)
            if len(err) > 0: on_progress(err)

        if on_progress:
            process.readyReadStandardOutput.connect(progress)
            process.readyReadStandardError.connect(progress)

        process.start(pgsql2shp_cmd)


'''
parse and return the complete data, projcs and geogcs description out of a given .prj file
'''
def parse_projection_file(filename):
    with open(filename) as f:
        data = f.read()
        projcs, geogcs = parse_projection_data(data)

    return data, projcs, geogcs

'''
parse and return the projcs and geogcs description out of a projection-string
'''
def parse_projection_data(data):

    projcs_pattern = 'PROJCS\["(.*?)",'
    projcs_matches = re.findall(projcs_pattern, data)
    geogcs_pattern = 'GEOGCS\["(.*?)",'
    geogcs_matches = re.findall(geogcs_pattern, data)

    projcs = projcs_matches[0] if len(projcs_matches) > 0 else None
    geogcs = geogcs_matches[0] if len(geogcs_matches) > 0 else None

    return projcs, geogcs
