# -*- coding: utf-8 -*-

import pandas as pd
from visumtransfer.visum_table import VisumTable


class Modus(VisumTable):
    name = 'Modi'
    code = 'MODUS'
    _cols = 'CODE;NAME;VSYSSET;AUSTAUSCHBAR'


class Nachfragemodell(VisumTable):
    name = 'Nachfragemodelle'
    code = 'NACHFRAGEMODELL'
    _cols = 'CODE;NAME;TYP;MODUSSET'


class Strukturgr(VisumTable):
    name = 'Strukturgrößen'
    code = 'STRUKTURGROESSE'
    _cols = 'CODE;NAME;NACHFRAGEMODELLCODE'

    def create_tables(self,
                      activities: pd.DataFrame,
                      model: str,
                      suffix=''):
        rows = []
        for idx, a in activities.iterrows():
            # Heimataktivität hat keine Strukturgröße
            if not a['potential']:
                continue
            row = self.Row(nachfragemodellcode=model)
            row.code = a['potential'] + suffix
            row.name = a['name']
            rows.append(row)
        self.add_rows(rows)


class Strukturgroessenwert(VisumTable):
    name = 'Strukturgrößenwerte'
    code = 'STRUKTURGROESSENWERT'
    _cols = 'BEZNR;STRUKTURGROESSENCODE;WERT'
    _longformat = True
    _mode = ''


class PersonengruppeJeBezirk(VisumTable):
    name = 'Personengruppe je Bezirk'
    code = 'PERSONENGRUPPEJEBEZIRK'
    _cols = 'BEZNR;PGRUPPENCODE;ANZPERSONEN'
    _longformat = True
    _mode = ''


class Nachfragebeschreibung(VisumTable):
    name = 'Nachfragebeschreibungen'
    code = 'NACHFRAGEBESCHREIBUNG'
    _cols = 'NSEGCODE;NACHFRAGEGLNR;MATRIX'
    _defaults = {'NACHFRAGEGLNR': 1}
