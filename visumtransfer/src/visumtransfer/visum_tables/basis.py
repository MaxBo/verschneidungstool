# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from visumtransfer.visum_table import VisumTable



class Netz(VisumTable):
    name = 'Netz'
    code = 'NETZ'
    _mode = ''
    _cols = ''
    _pkey = ''

    @property
    def pkey(self):
        return None

    def validate_df(self, df: pd.DataFrame):
        """Validate the DataFrame, may be defined differently in the subclass"""
        if len(self.df) > 1:
            raise ValueError(f'{self.__class__} may have only one row')


class BenutzerdefiniertesAttribut(VisumTable):
    name = 'Benutzerdefinierte Attribute'
    code = 'BENUTZERDEFATTRIBUTE'

    _cols = ('OBJID;ATTID;CODE;NAME;DATENTYP;MINWERT;MAXWERT;'
    'STANDARDWERT;STRINGSTANDARDWERT;KOMMENTAR;MAXSTRINGLAENGE;ANZDEZSTELLEN;'
    'DATENQUELLENTYP;FORMEL;QUERSCHNITTSLOGIK')

    _pkey = 'OBJID;ATTID'

    _defaults = {'DATENTYP': 'Double',
                 'QUERSCHNITTSLOGIK': 'SUM',
                 'ANZDEZSTELLEN': 3,
                 'MAXSTRINGLAENGE': 255,
                 'MINWERT': 'MIN',
                 'MAXWERT': 'MAX',
                 }

    def add_formel_attribute(self,
                             objid,
                             name,
                             formel,
                             attid=None,
                             code=None,
                             **kwargs):
        """
        add Formel-Attribut

        Parameters
        ----------
        objid : str
            the network type like NETZ, AKTIVITAET etc.
        name : str
            the name of the attribute, will be used as code and attid, too,
            if they are not explicitely specified
        formel : str
            the formula
        attid : str, optional
            the attid. If None, the code, and if the code is None, name will be taken
        code : str, optional
            the code. If None, the name will be taken
        """
        attid = attid or code or name
        code = code or name
        row = self.Row(objid=objid,
                       datenquellentyp='FORMEL',
                       name=name,
                       attid=attid,
                       code=code,
                       formel=formel,
                       **kwargs)
        self.add_row(row)

    def add_daten_attribute(self,
                            objid,
                            name,
                            attid=None,
                            code=None,
                            **kwargs):
        """
        add Daten-Attribut

        Parameters
        ----------
        objid : str
            the network type like NETZ, AKTIVITAET etc.
        name : str
            the name of the attribute, will be used as code and attid, too,
            if they are not explicitely specified
        attid : str, optional
            the attid. If None, the code, and if the code is None, name will be taken
        code : str, optional
            the code. If None, the name will be taken
        """
        attid = attid or code or name
        code = code or name
        row = self.Row(objid=objid,
                       datenquellentyp='DATEN',
                       name=name,
                       attid=attid,
                       code=code,
                       **kwargs)
        self.add_row(row)



class Verkehrssystem(VisumTable):
    name = 'Verkehrssysteme'
    code = 'VSYS'

    _cols = ('CODE;TYP')


class Oberbezirk(VisumTable):
    name = 'Oberbezirke'
    code = 'OBERBEZIRK'
    _cols = 'NR;XKOORD;YKOORD'


class Bezirke(VisumTable):
    name = 'Bezirke'
    code = 'BEZIRK'
    _cols = 'NR'

    def read_pgr(self, fn):
        r = np.recfromtxt(open(fn, mode='rb').readlines(), delimiter=',',
                          names=True, filling_values=0)
        names = r.dtype.names[2:]
        attrs = [f'NumPersons({pg})' for pg in names]
        self._cols = ';'.join(['NO'] + attrs)

        values = r[['vz_id']+list(names)]
        self.add_rows(values.tolist())
        self._mode = '*'

    def read_strukturdaten(self, fn):
        r = np.recfromtxt(open(fn, mode='rb').readlines(), delimiter=',',
                          names=True, filling_values=0)
        names = r.dtype.names[2:]
        attrs = [f'ValStructuralProp({sg.lstrip("ValStructuralProp")})'
                 if sg.startswith('ValStructuralProp')
                 else sg
                 for sg in names]
        self._cols = ';'.join(['NO'] + list(attrs))

        values = r[['vz_id']+list(names)]
        self.add_rows(values.tolist())
        self._mode = '*'
