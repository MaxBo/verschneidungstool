# -*- coding: utf-8 -*-

import datetime
import csv
from collections import OrderedDict
from typing import Dict, Iterable, List
from copy import copy
import os
import io
import numpy as np
from recordclass import recordclass
import pandas as pd
from visumtransfer.visum_attributes import VisumAttributes


class VisumTables:
    """Singleton to store all tables"""
    _instance = None  # Keep instance reference
    tables: Dict[str, 'VisumTable']
    visum_attributes: VisumAttributes

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.tables = OrderedDict()
            cls.add_visum_attributes()
        return cls._instance

    @classmethod
    def add_visum_attributes(cls):
        """add visum attributes"""
        fn_attrs_h5 = os.path.join(os.path.dirname(__file__), 'attributes.h5')
        try:
            cls.visum_attributes = VisumAttributes.from_hdf(fn_attrs_h5)
        except IOError:
            cls.visum_attributes = VisumAttributes.from_excel(fn_attrs_h5)


class WriteLine:
    """Wrapper around file object"""
    def __init__(self, fobj: io.TextIOWrapper):
        self.fobj = fobj

    def writeln(self, text: str):
        """write text to open `fobj`"""
        print(text, file=self.fobj)


class MetaClass(type):
    """Metaclass to register VisumTable with the VisumTables-Singleton"""
    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaClass, cls).__new__(cls, clsname, bases, attrs)
        # register with VisumTables
        VisumTables().tables[newclass.code] = newclass
        return newclass


class VisumTable(metaclass=MetaClass):
    """A VisumTable"""
    name = ''
    code = ''
    _cols = ''
    _pkey = ''
    _modes = {'': '',
              '*': ' (geändert)',
              '+': ' (eingefügt)',
              '-': ' (gelöscht)',
              '!': '',
              }
    _mode = '+'
    _defaults = {}
    _longformat = False

    # map Umlaute to normal letters
    _intab = "-()äöüÄÖÜß"
    _outtab = "___aouAOUs"
    _converters = {}

    def __init__(self, mode: str = None, new_cols: List[str] = None):
        """
        Parameters
        ----------
        mode : str, optional

          + -> new objects
          * -> change existing objects
          - -> delete objects

        cols: List[str], optional
            append the cols to the existing cols
        """
        if new_cols:
            self._cols = ','.join(self.cols + new_cols).strip(',')

        if mode is not None:
            self._mode = mode
        self._df = pd.DataFrame()

        # define the trantab for the column names

        self.trantab = str.maketrans(self._intab, self._outtab)

        # define row as a recordclass with default-values
        self.define_row()

    def copy(self) -> 'VisumTable':
        """copy myself"""
        return copy(self)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, df: pd.DataFrame):
        self.validate_df(df)
        self._df = df

    def validate_df(self, df: pd.DataFrame):
        """Validate the DataFrame, may be defined differently in the subclass"""

    @property
    def converters(self) -> Dict[str, callable]:
        """
        return converter dict for pandas.read_csv
        for those columns that are in `self._converters`
        then function
        - strips the the value in `self._converter` from the value passed
        - converts ',' to '.' as decimal
        - converts the string into a float

        Examples
        --------
        MyTable(VisumTable)
        _converters={'LENGTH': 'km'}

        then 0,234km is returned as the float 0.234
        """
        converters = {}
        for k, v in self._converters.items():
            def func(value):
                stripped = value.rstrip(v).replace(',', '.')
                try:
                    return float(stripped)
                except ValueError:
                    return np.NAN
            converters[k] = func
        return converters

    def unconvert(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """unconvert the columns marked in the dataframe"""
        if df is None:
            df = self.df
        for colname in self.df.columns:
            unit = self._converters.get(colname, None)
            if unit:
                column = df[colname]
                is_na = column.isna()
                str_column = column.map(f'{{:,.3f}}{unit}'.format)
                df[colname] = str_column
                df.loc[is_na, colname] = ''
            if self.is_bool(colname):
                column = df[colname]
                is_na = ~column.isna()
                df[colname] = column.fillna('')
                df.loc[is_na, colname] = column.loc[is_na].astype(int)
        return df

    def define_row(self):
        """
        set the Row-object for the table as a recordclass
        defined by the column names and the default values
        """
        self.Row = recordclass(typename=self.code,
                               fields=[c.lower().translate(self.trantab)
                                       for c in self.cols])
        self.Row.__new__.__defaults__ = tuple(self._defaults.get(c.upper(), '')
                                              for c in self.cols)

    @property
    def cols(self) -> List[str]:
        return self._cols.replace('\\', '_').split(';')

    @property
    def pkey(self):
        if not self._pkey:
            # assume that the first column is the primary key
            return self.cols[0]
        return self._pkey.split(';')

    def write_block(self, fobj: WriteLine, columns: str = None):
        """
        write a block of code to `fobj`

        Parameters
        ----------
        fobj: WriteLine-instance
            holding the open file stream
        columns: str, optional
            the columns to write
        """
        self.write_block_header(fobj)
        self.write_df(fobj, columns)

    def write_df(self, fobj: WriteLine, columns: str = None):
        """
        Write .df-Object to open file
        Parameters
        ----------
        fobj: WriteLine-instance
            holding the open file stream
        columns: str, optional
            the columns to write
        """
        if self.df.index.names == [None]:
            df = self.df
        else:
            df = self.df.reset_index()

        if columns:
            df = df[columns.split(';')]

        df = self.unconvert(df)

        cols = columns or ';'.join(c for c in df.columns)
        fobj.writeln(f'${self._mode}{self.code}:{cols}')

        df.to_csv(fobj.fobj,
                  sep=';',
                  quoting=csv.QUOTE_NONE,
                  header=False,
                  index=False,
                  lineterminator='\n')
        fobj.writeln('')

    @property
    def tablename(self) -> str:
        """get the english tablename"""
        visum_attributes = VisumTables().visum_attributes
        tables = visum_attributes.tables.reset_index().set_index('Long(DEU)')
        try:
            row = tables.loc[self.name]
        except KeyError:
            raise KeyError(f'table {self.name} not in attributes.xlsx')
        return row.Name

    def is_bool(self, colname: str) -> bool:
        """"""
        visum_attributes = VisumTables().visum_attributes
        attrs = visum_attributes.attributes
        try:
            row = attrs.loc[self.tablename, colname]
        except KeyError:
            return False
        return row.ValueType == 'bool'

    def write_block_header(self, fobj: WriteLine):
        """Write header for block to `fobj`"""
        fobj.writeln('*')
        fobj.writeln(f'* Tabelle: {self.name}{self._modes[self._mode]}')
        fobj.writeln('*')

    def df_from_array(self, data_arr) -> pd.DataFrame:
        df = pd.DataFrame(data_arr, columns=self.cols)
        if self.pkey:
            df.set_index(self.pkey, inplace=True)
        return df

    def df_from_string(self, data_str: str) -> pd.DataFrame:
        data_arr = [r.split(';') for r in data_str.split(os.linesep)]
        df = self.df_from_array(data_arr)
        return df

    def add_row(self, row: recordclass):
        self.add_rows([list(row)])

    def add_rows(self, rows: List[recordclass]):
        df2append = self.df_from_array(rows)
        self.df = pd.concat([self.df, df2append], verify_integrity=True)

    def add_df(self, df: pd.DataFrame):
        """Add a pandas Dataframe"""
        df.columns = df.columns.str.upper()
        df = df\
            .reset_index()\
            .reindex(self.cols, axis='columns')\
            .set_index(self.pkey)\
            .fillna(self._defaults)
        self.df = self.df.append(df, verify_integrity=True)

    def add_cols(self, new_cols: list):
        """Add columns to the columns definition"""
        self._cols = ';'.join(np.concatenate([self.cols, new_cols]))
        self.define_row()

    def __len__(self) -> int:
        return len(self.df)

    def __repr__(self):
        return f'{self.name} ({self._mode}{len(self)})'

    def update_original_df(self, new_df: pd.DataFrame):
        """
        Update Dataframe with the new dataframe `new_df`, keeping the
        original columns and using self.new_df to append the new rows

        Parameters
        ----------
        new_df : pd.Dataframe
        """
        # init the new dataframe
        if not hasattr(self, 'new_df'):
            self.new_df = self.df.reset_index().iloc[:0].set_index(self.pkey)
        columns = self.df.columns
        print(self.df.shape, new_df.shape)
        add_df = new_df.reset_index()[columns].set_index(self.pkey)
        new_rows = add_df[~add_df.index.isin(self.new_df.index)]
        self.new_df = self.new_df.append(new_rows)
        print(self, new_rows.shape, self.new_df.shape)


TablesDict = Dict[str, VisumTable]


class Version(VisumTable):
    name = 'Versionsblock'
    code = 'VERSION'
    _cols = 'VERSNR;FILETYPE;LANGUAGE;UNIT'
    _defaults = {
        'VERSNR': 10.0,
        'LANGUAGE': 'DEU',
        'FILETYPE': 'Demand',
        'UNIT': 'KM',
                     }
    _mode = ''

    def add_netfile_header(self):
        """add header for a netfile"""
        row = self.Row()
        self.add_row(row)

    def add_transfile_header(self):
        """add header for a netfile"""
        row = self.Row(filetype='Trans')
        self.add_row(row)


class VisumTransfer:
    """
    Class VisumTransfer holds the information on the sections in a transfer file
    in self.tables
    """
    def __init__(self,
                 user: str,
                 date=None,
                 sep: str = ';'):
        self.user = user
        self.date = date or datetime.date.today()
        self.tables = OrderedDict()  # type: TablesDict
        self.decimal = '.'
        self.sep = sep

    def __repr__(self):
        return f'VisumTransfer with {len(self.tables)} tables'

    @classmethod
    def new_transfer(cls,
                     user: str = 'Gertz Gutsche Rümenapp '
                     'Stadtentwicklung und Mobilität GbR Hamburg'
                     ) -> 'VisumTransfer':
        self = cls(user=user)
        version = Version()
        version.add_transfile_header()
        self.add_table(version, name='Version')
        return self

    def add_table(self, table: VisumTable, name: str = ''):
        """
        Add a visum-table with given name to self.tables
        if name is not given, it is derived from the VisumTable
        """
        name = name or table.code
        self.tables[name] = table

    def get_dataframes(self, code: str, mode: str = '') -> pd.DataFrame:
        """
        return a dataframe with all tables merged of Visum-Type `code`
        and modification-type `mode`
        """
        df = pd.DataFrame()
        for name, table in self.tables.items():
            if table.code == code and table._mode == mode:
                df = df.append(table.df)
        return df

    def get_tables(self, code: str, modes: Iterable = '') -> TablesDict:
        """
        return a dict of tables of Visum-Type `code`
        and modification-type in `modes`
        """
        tables = {name: table
                  for name, table in self.tables.items()
                  if table.code == code and table._mode in modes}
        return tables

    def write_modification(self, number: int, modification_folder: str):
        """Write a modification file with the given number"""
        fn = self.get_modification(number, modification_folder)
        self.write(fn)

    def write(self, fn: str):
        """Write transfer file to file `fn`"""
        with open(fn, 'w') as f:
            fobj = WriteLine(f)
            fobj.writeln('$VISION')
            fobj.writeln(f'* {self.user}')
            fobj.writeln(f'* {self.date}')
            for table in self.tables.values():
                table.write_block(fobj)

    def append(self, fn: str):
        """Append tables except the VERSION-section to the existing transfer file `fn`"""
        with open(fn, 'a') as f:
            fobj = WriteLine(f)
            for table in self.tables.values():
                #  skip Version when appending to existing tra-file
                if table.code == 'VERSION':
                    continue
                table.write_block(fobj)

    def get_modification(self, number: int, modification_folder: str) -> str:
        """return the modification file path"""
        fn = f'M{number:06d}.tra'
        fpath = os.path.join(modification_folder, fn)
        return fpath

    @property
    def visum_tables(self) -> Dict[str, VisumTable]:
        return VisumTables().tables

    def read_from_modification(self,
                               filename: str,
                               sections_to_read: List[str] = None,
                               decimal: str = '.'):
        """read visum-demand from modification file"""
        position = 0
        with open(filename, 'rb') as f:
            li = f.readline().decode('cp1252').strip()
            if not li == '$VISION':
                raise ValueError(
                    f'file {filename} is no Visum-Modification file')
            section = ''
            for line in f:
                li = line.decode('cp1252').strip()
                if not li or li.startswith('*'):
                    continue
                if li.startswith('$'):
                    position = f.tell()
                    if hasattr(self, 'current_table'):
                        self.current_table._endpos = position - len(line)
                    full_section, cols, = li.split(':')
                    mode = ''
                    if full_section[1] in VisumTable._modes:
                        mode = full_section[1]
                        section = full_section[2:].upper()
                    else:
                        mode = ''
                        section = full_section[1:].upper()

                    i = 1
                    section_name = section
                    while section_name in self.tables:
                        section_name = f'{section}_{i}'
                        i += 1
                    self.current_table = self.visum_tables[section](mode=mode)
                    self.current_cols = cols.translate(
                        self.current_table.trantab).split(self.sep)
                    self.current_table._cols = ';'.join(cols.split(self.sep))
                    self.current_table.define_row()
                    self.current_table._startpos = position
                    self.add_table(self.current_table, name=section_name)
                elif sections_to_read and section not in sections_to_read:
                    continue

            position = f.tell()
            self.current_table._endpos = position

            for tablename, table in self.tables.items():
                f.seek(table._startpos)
                lines = f.read(table._endpos -
                               table._startpos).decode('cp1252')
                buf = io.StringIO(lines)
                df = pd.read_csv(buf,
                                 names=table.cols,
                                 comment='*',
                                 delimiter=self.sep,
                                 decimal=decimal,
                                 converters=table.converters,
                                 )
                table.df = df
