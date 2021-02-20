# -*- coding: utf-8 -*-

import datetime
from collections import defaultdict
import xarray as xr
from visumtransfer.params import Params
from typing import Mapping
from .basis import BenutzerdefiniertesAttribut
from visumtransfer.visum_table import VisumTable


class MatrixCategories(dict):
    _end_block: Mapping[str, int] = {
        'Start': 10000,
        'General': 10005,
        'Visem_Demand': 10020,
        'Visem_OV_Stunden': 10030,
        'Other_Demand': 10090,
        'OV_Demand': 10100,
        'DestinationChoiceSkims': 10110,
        'IV_Skims': 10150,
        'IV_Skims_Parking': 10200,
        'OV_Skims_Fare': 10250,
        'OV_Skims_PJT': 10700,
        'Activities': 10800,
        'Activities_Homebased': 10900,
        'Activities_Balancing': 11000,
        'Commuters': 11100,
        'VL_Activities': 11200,
        'VL_Activities_Homebased': 11300,
        'VL_Activities_OBB': 11600,
        'Activities_OBB': 11700,
        'OV_TimeSeries_Skims_Formula': 11800,
        'OV_TimeSeries_Skims': 12000,
        'Demand_Pgr': 14000,
        'VL_Pgr': 16000,
        'Demand_Wiver': 17000,
        'Demand_Wiver_OBB': 17500,
        'OV_Demand_Activities': 18000,
        'Modes_Demand_Activities': 19000,
        'Demand_OV_Tagesgang': 20000,
        'Demand_Verkehrsleistung': 22000,
        'LogsumsPendler': 24000,
        'Logsums': 25000,
        'Accessibilities': 30000,
    }

    def __init__(self):
        start_idx = 1
        for category, end_idx in sorted(
          self._end_block.items(), key=lambda x: x[1]):
            self[category] = iter(range(start_idx, end_idx))
            # next block starts where the last ends
            start_idx = end_idx
        self['_fallback'] = iter(range(start_idx, 9999999))


class Matrix(VisumTable):
    name = 'Matrizen'
    code = 'MATRIX'
    matrix_category = ''

    _cols = ('NR;CODE;NAME;MATRIXTYP;BEZUGSTYP;NSEGCODE;NSCHICHTSET;DATNAME;'
    'ANZDEZSTELLEN;DATENQUELLENTYP;FORMEL;TAG;VONZEIT;BISZEIT;ZEITBEZUG;'
    'MODUSCODE;MODUSSET;PERSONENGRUPPENSET;PGRUPPENCODE;AKTIVCODE;'
    'QUELLAKTIVITAETSET;ZIELAKTIVITAETSET;'
    'INITMATRIX;SAVEMATRIX;LOADMATRIX;MATRIXFOLDER;'
    'CALIBRATIONCODE;NACHFRMODELLCODE;CATEGORY;OBB_MATRIX_REF')

    _defaults = {'ANZDEZSTELLEN': 2,
                 'MATRIXTYP': 'Nachfrage',
                 'BEZUGSTYP': 'Bezirk',
                 'INITMATRIX': 0,
                 'SAVEMATRIX': 0,
                 'LOADMATRIX': 0,
                 }

    def __init__(self):
        super().__init__()
        self._number_block = MatrixCategories()

    def set_category(self, matrix_category: str):
        """Set set matrix_category"""
        self.matrix_category = matrix_category

    @property
    def matrix_numbers(self) -> MatrixCategories:
        return self._number_block[self.matrix_category]

    def next_number(self) -> int:
        """Return next matrix number in range"""
        try:
            nr = next(self.matrix_numbers)
        except StopIteration:
            nr = next(self._number_block['_fallback'])
        return nr

    def add_daten_matrix(self,
                         code: str,
                         name='',
                         loadmatrix=0,
                         matrixfolder='',
                         datname='',
                         category: str = None,
                         **kwargs) -> int:
        """
        add Daten-Matrix

        Parameters
        ----------
        code : str
            the code of the matrix
        name : str, optional
            the name of the matrix. If not provided, the code is taken as name
        loadmatrix : int, optional(default=0)
            1 if matrix should be loaded
        matrixfolder : str, optional
            if given, read/write from Common Project folder, else from Scenario
        datname : str, optional
            the filename of the matrix on disk.
            If not provided, the code is taken as name
        category : str, optional
            the matrix category. If not given,
            use the category last set by set_category()

        Returns
        -------
        nr : int
            the number of the matrix inserted
        """
        name = name or code
        datname = datname or code
        nr = self.next_number()
        row = self.Row(nr=nr,
                       code=code,
                       name=name,
                       datenquellentyp='DATEN',
                       loadmatrix=loadmatrix,
                       matrixfolder=matrixfolder,
                       datname=datname,
                       category=category or self.matrix_category,
                       ** kwargs)
        self.add_row(row)
        return nr

    def add_formel_matrix(self,
                          code: str,
                          formel: str,
                          name='',
                          datname='',
                          category: str = None,
                          **kwargs) -> int:
        """
        add Formel-Matrix

        Parameters
        ----------
        code : str
            the code of the matrix
        formel : str
            the formula
        name : str, optional
            the name of the matrix. If not provided, the code is taken as name
        datname : str, optional
            the filename of the matrix if it is stored on disk.
            If not provided, the code is taken as name
        category : str, optional
            the matrix category. If not given,
            use the category last set by set_category()
        **kwargs
            other columns

        Returns
        -------
        nr : int
            the number of the matrix inserted
       """
        name = name or code
        datname = datname or code
        nr = self.next_number()
        row = self.Row(nr=nr,
                       code=code,
                       formel=formel,
                       name=name,
                       loadmatrix=0,
                       datenquellentyp='FORMEL',
                       datname=datname,
                       category=category or self.matrix_category,
                       **kwargs)
        self.add_row(row)
        return nr

    def get_timestring(self, hour: float) -> str:
        """
        convert hour into a time string in format HH:MM:SS
        """
        hour, minute, second = self._get_time_hour_minute_second(hour)
        t = datetime.time(hour, minute, second)
        return t.strftime('%H:%M:%S')

    def _get_time_hour_minute_second(self, hour):
        minute = (hour % 1) * 60
        hour = int(hour)
        if hour >= 24:
            hour = 23
            minute = 59
            second = 59
        else:
            second = int(round((minute % 1) * 60, 0))
            minute = int(minute)

        return hour, minute, second

    def get_time_seconds(self, hour: float) -> float:
        """
        convert hour into seconds since 00:00:00
        """
        hour, minute, second = self._get_time_hour_minute_second(hour)
        seconds = hour * 3600 + minute * 60 * + second
        return seconds

    def add_ov_kg_matrices(self,
                           params: Params,
                           userdef: BenutzerdefiniertesAttribut,
                           savematrix=0,
                           factor=.8,
                           exponent=.8,
                           time_interval=1,
                           tag_index: int = 1,
                           ):
        """Add OV Kenngrößen-Matrizen für Zeitscheiben"""
        time_series = params.time_series
        nsegcode = 'OEV'
        self.set_category('OV_TimeSeries_Skims')
        for idx, ts in time_series.iterrows():
            ts_code = ts.code
            ts_name = ts.name_long
            vonzeit = self.get_timestring(ts.from_hour)
            biszeit = self.get_timestring(ts.to_hour)
            self.add_daten_matrix(
                code='PJT',
                matrixtyp='Kenngröße',
                name=f'Empfundene Reisezeit {nsegcode} {ts_name}',
                datname=f'PJT_{ts_code}',
                nsegcode=nsegcode,
                tag=tag_index,
                vonzeit=vonzeit,
                biszeit=biszeit,
                zeitbezug='Abfahrtszeit',
                initmatrix=1,
                # moduscode='O'
            )
            self.add_daten_matrix(
                code='FAR',
                matrixtyp='Kenngröße',
                name=f'Fahrpreis {nsegcode} {ts_name}',
                datname=f'FAR_{ts_code}',
                nsegcode=nsegcode,
                tag=tag_index,
                vonzeit=vonzeit,
                biszeit=biszeit,
                initmatrix=1,
                zeitbezug='Abfahrtszeit',
                # moduscode='O',
            )
            self.add_daten_matrix(
                code='FFZ',
                matrixtyp='Kenngröße',
                name=f'Fahrzeugfolgezeit {nsegcode} {ts_name}',
                datname=f'FFZ_{ts_code}',
                nsegcode=nsegcode,
                tag=tag_index,
                vonzeit=vonzeit,
                biszeit=biszeit,
                initmatrix=1,
                zeitbezug='Abfahrtszeit',
                # moduscode='O',
            )
            self.add_daten_matrix(
                code='JRD',
                matrixtyp='Kenngröße',
                name=f'Reiseweite {nsegcode} {ts_name}',
                datname=f'JRD_{ts_code}',
                nsegcode=nsegcode,
                tag=tag_index,
                vonzeit=vonzeit,
                biszeit=biszeit,
                initmatrix=1,
                zeitbezug='Abfahrtszeit',
                # moduscode='O',
            )

        self.add_daten_matrix(
            code='PJT',
            matrixtyp='Kenngröße',
            name=f'Empfundene Reisezeit {nsegcode}',
            nsegcode=nsegcode,
            vonzeit='',
            biszeit='',
            zeitbezug='Abfahrtszeit',
            # moduscode='O',
        )
        #self.add_daten_matrix(
            #code='FAR',
            #matrixtyp='Kenngröße',
            #name=f'Fahrpreis {nsegcode}',
            #nsegcode=nsegcode,
            #vonzeit='',
            #biszeit='',
            #zeitbezug='Abfahrtszeit',
            ## moduscode='O',
        #)
        self.add_daten_matrix(
            code='FFZ',
            matrixtyp='Kenngröße',
            name=f'Fahrzeugfolgezeit {nsegcode}',
            nsegcode=nsegcode,
            vonzeit='',
            biszeit='',
            zeitbezug='Abfahrtszeit',
            # moduscode='O',
        )
        #self.add_daten_matrix(
            #code='XADT',
            #matrixtyp='Kenngröße',
            #name=f'Erweiterte Anpassungszeit {nsegcode}',
            #nsegcode=nsegcode,
            #vonzeit='',
            #biszeit='',
            #zeitbezug='Abfahrtszeit',
            ## moduscode='O',
        #)
        self.set_category('OV_TimeSeries_Skims_Formula')

        self.add_daten_matrix(
            code='No_Connection_Forward',
            matrixtyp='Kenngröße',
            name='Keine ÖV-Verbindung in Zeitscheibe Hinweg',
            nsegcode=nsegcode,
            moduscode='O',
        )
        self.add_daten_matrix(
            code='No_Connection_Backward',
            matrixtyp='Kenngröße',
            name='Keine ÖV-Verbindung in Zeitscheibe Rückweg',
            nsegcode=nsegcode,
            moduscode='O',
        )
        # ÖV-Kosten
        self.set_category('OV_Skims_Fare')
        self.add_daten_matrix(
            code='SINGLETICKET',
            matrixtyp='Kenngröße',
            name='Fahrpreis Einzelticket',
            datname='Singelticket',
            nsegcode=nsegcode,
            moduscode='O',
            loadmatrix=0,
            savematrix=savematrix,
        )

        #self.add_daten_matrix(
            #code='JRD',
            #matrixtyp='Kenngröße',
            #name=f'Reiseweite {nsegcode}',
            #nsegcode=nsegcode,
            #vonzeit='',
            #biszeit='',
            ## initmatrix=1,
            #zeitbezug='Abfahrtszeit',
            ## moduscode='O',
        #)

        self.add_daten_matrix(
            code='OVDIS',
            matrixtyp='Kenngröße',
            name='OV Reiseweite',
            datname='OVDIS',
            nsegcode=nsegcode,
            loadmatrix=0,
            savematrix=savematrix,
            moduscode='O',
        )

        userdef.add_daten_attribute('Netz', 'DistanceKorrBisKm_OV',
                                         standardwert=3)
        userdef.add_daten_attribute('Netz', 'DistanceKorrFaktor_OV',
                                         standardwert=-1.5)

        self.add_formel_matrix(
            code='DistanzKorrektur_OV',
            matrixtyp='Kenngröße',
            name='DistanzKorrektur_OV',
            datname='DistanzKorrektur_OV',
            moduscode='O',
            formel='(Matrix([CODE] = "KM") < [DistanceKorrBisKm_OV]) *'
            ' [DistanceKorrFaktor_OV] * '
            '([DistanceKorrBisKm_OV] - Matrix([CODE] = "KM"))',
        )

        # ÖV-Nachfragematrizen nach Zeitscheiben
        self.set_category('OV_TimeSeries_Skims_Formula')

        # PJT_All-Matrix für nur eine Zeitscheibe
        ts = time_series.loc[time_interval]
        ts_code = ts['code']
        vonzeit = self.get_time_seconds(ts['from_hour'])
        biszeit = self.get_time_seconds(ts['to_hour'])
        formula = (
            f'Matrix([CODE] = "PJT" & [FROMTIME]={vonzeit} & [TOTIME]={biszeit}) + '
            f'{factor} * POW('
            f'Matrix([CODE] = "FFZ" & [FROMTIME]={vonzeit} & [TOTIME]={biszeit})'
            f', {exponent})')

        complete_formula = f'(({formula}) + TRANSPOSE({formula})) * 0.5'

        self.add_formel_matrix(
            code='PJT_All',
            matrixtyp='Kenngröße',
            name='Empfundene Reisezeit alle Aktivitäten',
            nsegcode=nsegcode,
            formel=complete_formula,
        )

        self.add_formel_matrix(
            code='OWTS',
            matrixtyp='Kenngröße',
            name='Startwartezeit aus XADT',
            moduscode='O',
            formel='0.8 * POW(Matrix([CODE]="FFZ" & [FROMTIME]=21600 & [TOTIME]=32400):0.8)',
        )

    def add_iv_kg_matrices(self,
                           userdef: BenutzerdefiniertesAttribut,
                           savematrix=0):
        """Add PrT Skim Matrices"""
        self.set_category('IV_Skims')

        # TT0, TTC und DIS existieren schon
        #for nsegcode in ['P', 'PG']:
            #self.add_daten_matrix(code='DIS',
                                  #name=f'Fahrweite Pkw ({nsegcode})',
                                  #loadmatrix=1,
                                  #matrixtyp='Kenngröße',
                                  #nsegcode=nsegcode,
                                  #vonzeit='',
                                  #biszeit='',
                                  #savematrix=savematrix)
            #self.add_daten_matrix(code='TT0',
                                  #name=f't0 Pkw ({nsegcode})',
                                  #loadmatrix=1,
                                  #matrixtyp='Kenngröße',
                                  #nsegcode=nsegcode,
                                  #vonzeit='',
                                  #biszeit='',
                                  #savematrix=savematrix)
            #self.add_daten_matrix(code='TTC',
                                  #name=f'tAkt Pkw ({nsegcode})',
                                  #loadmatrix=1,
                                  #matrixtyp='Kenngröße',
                                  #nsegcode=nsegcode,
                                  #vonzeit='',
                                  #biszeit='',
                                  #savematrix=savematrix)

        self.add_daten_matrix(code='TFUSS', name='tFuss', loadmatrix=1,
                              matrixtyp='Kenngröße',
                              nsegcode='F',
                              moduscode='F',
                              savematrix=savematrix)
        self.add_daten_matrix(code='TRAD', name='tRad', loadmatrix=1,
                              matrixtyp='Kenngröße',
                              nsegcode='R',
                              moduscode='R',
                              savematrix=savematrix)
        self.add_daten_matrix(code='TTC_boxcox',
                              name='tAkt Pkw BoxCox-Transformiert',
                              loadmatrix=0,
                              matrixtyp='Kenngröße',
                              nsegcode='P',
                              moduscode='P',
                              savematrix=savematrix)

        userdef.add_formel_attribute(
            objid='Bezirk',
            name='Binnendistanz_area',
            formel='SQRT([FLAECHEKM2]) / 3',
            kommentar='geschätzte Binnendistanz in km',
                                    )

        self.add_formel_matrix(
            code='PkwKosten',
            matrixtyp='Kenngröße',
            nsegcode='P',
            name='Pkw Fahrtkosten',
            formel='Matrix([CODE] = "DIS" & [NSEGCODE] = "P") * '
                   '[COST_PER_KM_PKW]')

        self.add_formel_matrix(code='SFUSS', name='sFuss',
                               matrixtyp='Kenngröße',
                               nsegcode='F',
                               moduscode='F',
                               formel='Matrix([CODE] = "TFUSS") * 4.5 / 60')

        # Visum-Bug beim Einlesen der Formelmatrix
        formel = ('If (Matrix([CODE] = "TFUSS") > 100.0 : '
                  'If(Matrix([CODE] = "TRAD") < 999.0 : '
                  'Matrix([CODE] = "TRAD") * 16 / 60.0 : '
                  'Matrix([CODE] = "DIS" & [NSEGCODE] = "P")) : '
                  'Matrix([CODE] = "SFUSS"))')

        self.add_formel_matrix(code='KM', name='Reiseweite',
                                   matrixtyp='Kenngröße',
                                   formel=formel)

        userdef.add_daten_attribute('Netz', 'DistanceKorrBisKm_Pkw',
                                             standardwert=1.2)
        userdef.add_daten_attribute('Netz', 'DistanceKorrFaktor_Pkw',
                                             standardwert=-4)

        self.add_formel_matrix(
                code='DistanzKorrektur_Pkw',
                matrixtyp='Kenngröße',
                name='DistanzKorrektur_Pkw',
                datname='DistanzKorrektur_Pkw',
                moduscode='P',
                formel='(Matrix([CODE] = "KM") < [DistanceKorrBisKm_Pkw]) *'
                ' [DistanceKorrFaktor_Pkw] * '
                '([DistanceKorrBisKm_Pkw] - Matrix([CODE] = "KM"))',
            )


    def add_iv_demand(self, savematrix=0, loadmatrix=1):
        """Add PrT Demand Matrices"""
        mode_lkw = 'X'

        self.set_category('Visem_Demand')
        self.add_daten_matrix(code='Visem_P', name='Pkw regional',
                              loadmatrix=loadmatrix,
                              matrixtyp='Nachfrage',
                              nsegcode='P',
                              moduscode='P',
                              savematrix=savematrix,
                              obb_matrix_ref='[CODE]="Visem_OBB_P"',
                              matrixfolder='Analysefall',
                              )

        self.set_category('Other_Demand')
        # Wirtschaftsverkehr kommt aus LVMBY
        #self.add_daten_matrix(code='Pkw_Wirtschaftsverkehr',
                              #name='Pkw-Wirtschaftsverkehr',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='B_P',
                              #moduscode='P')
        #self.add_daten_matrix(code='Lieferfahrzeuge', name='Lieferfahrzeuge',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='B_Li',
                              #moduscode='P')
        #self.add_daten_matrix(code='Lkw_bis_12to',
                              #name='Lkw zw. 3,5 und 12 to',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='B_L1',
                              #moduscode=mode_lkw)
        #self.add_daten_matrix(code='Lkw_über_12to', name='Lkw > 3,5 to',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='B_L2',
                              #moduscode=mode_lkw)
        #self.add_daten_matrix(code='FernverkehrPkw',
                              #name='Pkw-Fernverkehr',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='PkwFern',
                              #moduscode='P')
        #self.add_daten_matrix(code='FernverkehrLkw',
                              #name='Lkw-Fernverkehr',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='LkwFern',
                              #moduscode=mode_lkw)

        ## Summen Schwerverkehr und Kfz bis 3.5 to
        #nsegs = ['Lkw_b_12 nwd',
                 #'Lkw_gr_12 nwd']
        #formel = ' + '.join((f'Matrix([CODE]="{nseg}" & [BEZUGSTYP]=2)'
                            #for nseg in nsegs))
        #self.add_formel_matrix(code='Schwerverkehr',
                               #formel=formel,
                               #name='Schwerverkehr ohne Busse',
                               #matrixtyp='Nachfrage',
                               #nsegcode='SV',
                               #moduscode=mode_lkw)

        #nsegs = ['Visem_P',
                 #'Pkw_Wirtschaftsverkehr',
                 #'PKW NWD',
                 #]
        #formel = ' + '.join((f'Matrix([CODE]="{nseg}" & [BEZUGSTYP]=2)'
                             #for nseg in nsegs))
        #self.add_formel_matrix(code='Kfz_35',
                               #formel=formel,
                               #name='Kfz bis 3,5 to',
                               #matrixtyp='Nachfrage',
                               #nsegcode='PG',
                               #moduscode='P')

    def add_ov_demand(self, savematrix=0, loadmatrix=1):
        """Add PrT Demand Matrices"""
        self.set_category('Visem_Demand')
        self.add_daten_matrix(code='Visem_O', name='ÖPNV',
                              loadmatrix=loadmatrix,
                              matrixtyp='Nachfrage',
                              nsegcode='OEV',
                              moduscode='O',
                              savematrix=savematrix,
                              obb_matrix_ref='[CODE]="Visem_OBB_O"',
                              matrixfolder='Analysefall',
                              )
        #self.set_category('OV_Demand')
        #self.add_daten_matrix(code='FernverkehrBahn', name='Fernverkehr Bahn',
                              #loadmatrix=loadmatrix,
                              #matrixtyp='Nachfrage',
                              #nsegcode='OFern',
                              #moduscode='O')

    def add_other_demand_matrices(self,
                                  params: Params,
                                  loadmatrix=1,
                                  savematrix=0):
        """Add Demand Matrices for other modes"""
        self.set_category('Visem_Demand')
        existing_codes = self.df['CODE'].tolist()

        matcode = 'Visem_Gesamt'
        matcode_obb = 'Visem_OBB_Gesamt'
        self.add_daten_matrix(code=matcode,
                              name='Gesamtwege Visem Region',
                              loadmatrix=loadmatrix,
                              savematrix=savematrix,
                              matrixtyp='Nachfrage',
                              obb_matrix_ref=f'[CODE]="{matcode_obb}"',
                              matrixfolder='Analysefall',
                              )
        self.add_daten_matrix(code=matcode_obb,
                              name='Gesamtwege Visem Region',
                              loadmatrix=0,
                              savematrix=0,
                              matrixtyp='Nachfrage',
                              bezugstyp='Oberbezirk')

        for m, mode in params.modes.iterrows():
            code = mode['code']
            mode_name = mode['name']
            matname = f'Wege {mode_name}'
            matcode = f'Visem_{code}'
            if matcode in existing_codes:
                continue
            self.add_daten_matrix(code=matcode,
                                  name=matname,
                                  loadmatrix=0,
                                  matrixtyp='Nachfrage',
                                  moduscode=code,
                                  savematrix=0,
                                  matrixfolder='Analysefall',
                                  obb_matrix_ref=f'[CODE]="Visem_OBB_{code}"',
                                  )


        for m, mode in params.modes.iterrows():
            code = mode['code']
            matcode = f'Visem_OBB_{code}'
            mode_name = mode['bezeichnung']
            name = f'Wege {mode_name} Oberbezirk Region'
            if matcode in existing_codes:
                continue
            self.add_daten_matrix(code=matcode,
                                  name=name,
                                  loadmatrix=0,
                                  matrixtyp='Nachfrage',
                                  moduscode=code,
                                  bezugstyp='Oberbezirk')

        self.set_category('Demand_Verkehrsleistung')
        for m, mode in params.modes.iterrows():
            distance_matrix = mode['distance_matrix']
            code = mode['code']
            matcode = f'VL_{code}'
            mode_name = mode['name']
            matname = f'Verkehrsleistung {mode_name}'
            nsegcode = mode['default_nsegcode']
            if nsegcode:
                cond_nsegcode = f' & [NSEGCODE] = "{nsegcode}"'
            else:
                cond_nsegcode = ''
            if matcode in existing_codes:
                continue
            formel = f'Matrix([CODE]="Visem_{code}") * '\
                f'Matrix([CODE]="{distance_matrix}"{cond_nsegcode})'
            matcode_obb = f'VL_OBB_{code}'
            self.add_formel_matrix(code=matcode,
                                   name=matname,
                                   formel=formel,
                                   matrixtyp='Nachfrage',
                                   moduscode=code,
                                   obb_matrix_ref=f'[CODE]="{matcode_obb}"',
                                   )
            self.add_daten_matrix(code=matcode_obb,
                                  name=name,
                                  loadmatrix=0,
                                  matrixtyp='Nachfrage',
                                  moduscode=code,
                                  bezugstyp='Oberbezirk')

    def add_ov_haupt_ap_demand_matrices(self,
                                        ds_tagesgang: xr.Dataset,
                                        loadmatrix=0,
                                        savematrix=1):
        """Add Demand Matrices for other modes"""
        self.set_category('Demand_OV_Tagesgang')
        for hap in ds_tagesgang.hap:
            matcode = f'Visem_OV_{hap.lab_hap.values}'
            self.add_daten_matrix(code=matcode,
                                  loadmatrix=loadmatrix,
                                  matrixtyp='Nachfrage',
                                  moduscode='O',
                                  savematrix=savematrix,
                                  )

    def add_commuter_matrices(self, userdef: BenutzerdefiniertesAttribut,
                              loadmatrix=1,
                              savematrix=1):
        """Add Commuter Matrices"""
        self.set_category('Commuters')
        self.add_daten_matrix(code='Pendlermatrix',
                              name='Pendlermatrix der BA disaggregiert auf Bezirke',
                              loadmatrix=0,
                              matrixtyp='Nachfrage',
                              matrixfolder='Pendler')
        self.add_daten_matrix(code='Pendlermatrix_OBB',
                              name='Pendlermatrix der BA (SvB)',
                              bezugstyp='Oberbezirk',
                              matrixtyp='Nachfrage',
                              loadmatrix=0,
                              matrixfolder='Pendler')
        formel = 'Matrix([CODE]="Pendlermatrix_OBB") * [SUM:PGRUPPEN\ERWERBSTAETIGE] '\
            '/ MATRIXSUM(Matrix([CODE] = "Pendlermatrix_OBB"))'
        #self.add_formel_matrix(
            #code='Pendlermatrix_OBB_Gesamt',
            #name='Pendlermatrix_OBB incl Nicht-SVB-Beschäftigte',
            #matrixtyp='Nachfrage',
            #bezugstyp='Oberbezirk',
            #matrixfolder='Pendler',
            #savematrix=0,
            #formel=formel)
        self.add_daten_matrix(
            code='Pendlermatrix_OBB_Gesamt',
            name='Pendlermatrix_OBB incl Nicht-SVB-Beschäftigte',
            matrixtyp='Nachfrage',
            bezugstyp='Oberbezirk',
            matrixfolder='Pendler',
            savematrix=0)

        self.set_category('DestinationChoiceSkims')
        self.add_formel_matrix(
            code='Aussen2Aussen',
            matrixtyp='Kenngröße',
            formel='-999999 * (FROM[TYPNR] > 3) * (TO[TYPNR] > 3)')
        self.add_formel_matrix(
            code='Innen2Aussen',
            matrixtyp='Kenngröße',
            formel='-999999 * ((FROM[TYPNR] <= 3) * (TO[TYPNR] <= 3) + (FROM[TYPNR] > 3) * (TO[TYPNR] > 3))')

    def add_logsum_matrices(self,
                            demand_strata: 'Nachfrageschicht',
                            actchains: 'Aktivitaetenkette',
                            matrix_range='Logsums',
                            ):
        """Add logsum matrices for each person group and main activity"""

        self.set_category(matrix_range)
        ketten = {ac_code: act['AKTIVCODES'].split(',')[1: -1]
                  for ac_code, act
                  in actchains.df.iterrows()}  # type: Mapping[str, List[str]]
        pgr_activities = defaultdict(set)  # type: Mapping[Tuple[str, str], set]
        for ds_code, ds in demand_strata.df.iterrows():
            pgr = ds['PGRUPPENCODES']
            nachfragemodellcode = ds['NACHFRAGEMODELLCODE']
            if nachfragemodellcode in ('VisemGGR', 'Pendler'):
                activities = pgr_activities[(nachfragemodellcode, pgr)]
                new_activities = ketten[ds['AKTKETTENCODE']]
                for activity in new_activities:
                    activities.add(activity)
        for (nmc, pgr), activities in pgr_activities.items():
            for activity in activities:
                code = 'LogsumMatrix'
                name = f'Logsum {pgr} {activity}'
                self.add_daten_matrix(
                    code,
                    name,
                    matrixtyp='Kenngröße',
                    loadmatrix=0,
                    savematrix=0,
                    initmatrix=1,
                    nachfrmodellcode=nmc,
                    pgruppencode=pgr,
                    aktivcode=activity,
                    )
