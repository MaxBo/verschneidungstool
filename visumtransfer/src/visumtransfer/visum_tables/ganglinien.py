# -*- coding: utf-8 -*-

import xarray as xr
import pandas as pd
from .demand import Nachfragebeschreibung
from .persongroups import Personengruppe
from visumtransfer.visum_table import VisumTable



class Ganglinienelement(VisumTable):
    name = 'Ganglinienelemente'
    code = 'GANGLINIENELEMENT'
    _cols = 'GANGLINIENNR;STARTZEIT;ENDZEIT;GEWICHT;MATRIX'
    _pkey = 'GANGLINIENNR;STARTZEIT;ENDZEIT'


class Nachfrageganglinie(VisumTable):
    name = 'NACHFRAGEGANGLINIE'
    code = 'NACHFRAGEGANGLINIE'
    _cols = 'NR;CODE;NAME;GANGLINIENNR'


class VisemGanglinie(VisumTable):
    name = 'VISEM-Ganglinien'
    code = 'VISEMGANGLINIE'
    _cols = 'AKTPAARCODE;PGRUPPENCODE;GANGLINIENNR'
    _pkey = 'AKTPAARCODE;PGRUPPENCODE'


class Ganglinie(VisumTable):
    name = 'Ganglinien'
    code = 'GANGLINIE'
    _cols = 'NR;NAME;WERTETYP'
    _defaults = {'WERTETYP': 'Anteile'}

    def create_tables(self,
                      activitypairs: pd.DataFrame,
                      time_series: pd.DataFrame,
                      ap_timeseries: pd.DataFrame,
                      ganglinienelement: Ganglinienelement,
                      nachfrageganglinie: Nachfrageganglinie,
                      visem_ganglinie: VisemGanglinie,
                      personengruppe: Personengruppe,
                      start_idx=100,
                      ):

        rows = []
        rows_ganglinienelement = []
        rows_nachfrageganglinien = []
        rows_visem_nachfrageganglinien = []
        ap_timeseries = ap_timeseries\
            .reset_index()\
            .set_index(['index', 'activitypair'])

        for a, ap in activitypairs.iterrows():
            ap_code = ap['code']
            idx = ap['idx']
            nr = idx + start_idx
            row = self.Row(nr=nr, name=ap_code)
            rows.append(row)

            # Nachfrageganglinie
            row_nachfrageganglinie = nachfrageganglinie.Row(
                nr=nr, code=ap_code, name=ap_code, gangliniennr=nr)
            rows_nachfrageganglinien.append(row_nachfrageganglinie)

            # Ganglinie
            ap_timeserie = ap_timeseries.iloc[idx]
            for t, ts in time_series.iterrows():
                from_hour = ts['from_hour']
                to_hour = ts['to_hour']
                anteil = ap_timeserie[from_hour:to_hour].sum()
                if anteil:
                    row_ganglinienelement = ganglinienelement.Row(
                        gangliniennr=nr,
                        startzeit=from_hour * 3600,
                        endzeit=to_hour * 3600,
                        gewicht=anteil)
                    rows_ganglinienelement.append(row_ganglinienelement)

            # Personengruppen
            for pg_code, pg in personengruppe.df.iterrows():
                row_visem_ganglinie = visem_ganglinie.Row(
                    pgruppencode=pg_code, gangliniennr=nr)
                if not pg['NACHFRAGEMODELLCODE'] == 'VisemGeneration':
                    row_visem_ganglinie.aktpaarcode = ap_code
                rows_visem_nachfrageganglinien.append(row_visem_ganglinie)

        self.add_rows(rows)
        ganglinienelement.add_rows(rows_ganglinienelement)
        nachfrageganglinie.add_rows(rows_nachfrageganglinien)
        visem_ganglinie.add_rows(rows_visem_nachfrageganglinien)


class Nachfragesegment(VisumTable):
    name = 'Nachfragesegments'
    code = 'NACHFRAGESEGMENT'
    _cols = 'CODE;NAME;MODUS'
    _defaults = {'MODUS': 'L'}

    def add_ov_ganglinien(self,
                          ds_ganglinie: xr.Dataset,
                          ganglinie: Ganglinie,
                          ganglinienelement: Ganglinienelement,
                          nachfrageganglinie: Nachfrageganglinie,
                          nachfrage_beschr: Nachfragebeschreibung,
                          start_idx: int = 80,
                          ):
        """Add Ganglinien for OV"""
        modus = 'O'
        rows_nseg = []
        rows_ganglinie = []
        rows_ganglinienelement = []
        rows_nachfrageganglinien = []
        rows_nachfragebeschreibung = []
        gl = ds_ganglinie.ganglinie
        ds_ganglinie['anteile_stunde'] = gl / gl.sum('stunde')

        for hap in ds_ganglinie.hap:
            hap_name = hap.lab_hap.values
            mat_code = f'Visem_OV_{hap_name}'

            nsg_code = f'OV_{hap_name}'
            nseg_name = f'OV {hap_name}'

            hap_id = hap.hap.values
            nachfr_gl_nr = gl_nr = hap_id + start_idx
            gl_name = f'OV_{hap_name}'
            rows_ganglinie.append(ganglinie.Row(nr=gl_nr, name=gl_name))

            row_nachfrageganglinie = nachfrageganglinie.Row(
                nr=nachfr_gl_nr, code=gl_name, name=gl_name,
                gangliniennr=gl_nr)
            rows_nachfrageganglinien.append(row_nachfrageganglinie)

            gl_stunde = ds_ganglinie.anteile_stunde.sel(hap=hap_id)

            for stunde in gl_stunde:
                # in sekunden, Intervalle von 60 sec.
                startzeit = stunde.stunde * 3600
                endzeit = startzeit + 3600
                if stunde:
                    row_ganglinienelement = ganglinienelement.Row(
                        gangliniennr=gl_nr,
                        startzeit=startzeit,
                        endzeit=endzeit,
                        gewicht=stunde)
                    rows_ganglinienelement.append(row_ganglinienelement)

            matrix_descr = f'MATRIX([CODE]="{mat_code}")'
            rows_nseg.append(self.Row(code=nsg_code,
                                      name=nseg_name,
                                      modus=modus))
            rows_nachfragebeschreibung.append(nachfrage_beschr.Row(
                nsegcode=nsg_code,
                nachfrageglnr=nachfr_gl_nr,
                matrix=matrix_descr
            ))

        self.add_rows(rows_nseg)
        ganglinie.add_rows(rows_ganglinie)
        nachfrageganglinie.add_rows(rows_nachfrageganglinien)
        ganglinienelement.add_rows(rows_ganglinienelement)
        nachfrage_beschr.add_rows(rows_nachfragebeschreibung)

