# -*- coding: utf-8 -*-

from .persongroups import Personengruppe
from .activities import Aktivitaet, Aktivitaetenkette
from visumtransfer.visum_table import VisumTable


class Nachfrageschicht(VisumTable):
    name = 'Nachfrageschichten'
    code = 'NACHFRAGESCHICHT'
    _cols = 'CODE;NAME;NACHFRAGEMODELLCODE;AKTKETTENCODE;PGRUPPENCODES;NSEGSET;MOBILITAETSRATE;TARIFMATRIX'

    def create_tables_gd(self,
                         personengruppe: Personengruppe,
                         aktivitaet: Aktivitaet,
                         aktivitaetenkette: Aktivitaetenkette,
                         nsegset: str = 'OEV,F,PM,P,R',
                         model: str = 'VisemGGR',
                         category: str = 'ZielVMWahl'):
        ac_hierarchy = aktivitaet.get_hierarchy()
        rows = []
        pgroups = personengruppe.df
        pgroups['TARIFMATRIX'].fillna('', inplace=True)
        pg_gd = pgroups.loc[pgroups['CATEGORY'] == category]
        for pgr_code, gd in pg_gd.iterrows():
            for ac_code, mobilitaetsrate in personengruppe.gd_codes[pgr_code]:
                dstratcode = ':'.join((pgr_code, ac_code))
                # get the main activity of the person group
                sequence = aktivitaetenkette.df.loc[ac_code, 'AKTIVCODES']
                main_act_code = aktivitaet.get_main_activity(ac_hierarchy, sequence)
                # take the tarifmatrix defined for the main activity
                tarifmatrix = aktivitaet.df.loc[main_act_code, 'TARIFMATRIX']
                for group_code in gd['GROUPS_CONSTANTS'].split(','):
                    # if there is a special tarifmatrix defined for a persongroup,
                    # take this one instead of the activity-Tarifmatrix
                    tarifmatrix = personengruppe.df.loc[group_code,
                                                        'TARIFMATRIX'] or tarifmatrix


                row = self.Row(code=dstratcode,
                               name=dstratcode,
                               nachfragemodellcode=model,
                               pgruppencodes=pgr_code,
                               aktkettencode=ac_code,
                               nsegset=nsegset,
                               mobilitaetsrate=mobilitaetsrate,
                               tarifmatrix=tarifmatrix,
                               )
                rows.append(row)
        self.add_rows(rows)
