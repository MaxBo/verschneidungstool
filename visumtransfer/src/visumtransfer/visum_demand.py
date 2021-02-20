# -*- coding: utf-8 -*-


import os
import json
import pandas as pd
from argparse import ArgumentParser

from visumtransfer.visum_table import (
    VisumTransfer)

from visumtransfer.visum_tables import (
    Netz,
    Modus,
    Matrix,
    BenutzerdefiniertesAttribut,
    Nachfragemodell,
    Strukturgr,
    Aktivitaet,
    Personengruppe,
    Aktivitaetenpaar,
    Aktivitaetenkette,
    Nachfrageschicht,
    Ganglinie,
    Ganglinienelement,
    Nachfrageganglinie,
    VisemGanglinie,
    Nachfragesegment
)

from visumtransfer.params import Params


class VisemDemandModel:
    """create a transfer file for a VisemModel"""
    def __init__(self,
                 modifications: str,
                 param_excel_fp: str):
        self.modifications = modifications
        self.params_excel_fp = param_excel_fp

    def create_transfer(self,
                        params: Params,
                        modification_number: int,
                        tag_index: int=1):
        """
        Create a Modification with the VISEM-Model and all elements needed

        Parameters
        ----------
        params : Params-instance
            the parameter to use
        modification_number: int
            the number used in M0000xx.tra
        tag_index: int
            the PuT-Matrices and time-series
            will use this day_index in the caledar to refer to
            the correct date
        """

        vt = VisumTransfer.new_transfer()

        modus = Modus()
        modus.add_row(
            modus.Row(code='O', name='ÖV', vsysset='BUS,F_X,S', austauschbar=True))
        modus.add_row(
            modus.Row(code='M', name='Pkw-Mitfahrer', vsysset='P', austauschbar=True))
        vt.tables['Modi'] = modus

        userdef1 = BenutzerdefiniertesAttribut()
        vt.tables['BenutzerdefinierteAttribute1'] = userdef1
        userdef2 = BenutzerdefiniertesAttribut()

        userdef1.add_daten_attribute('MATRIX', 'obb_matrix_ref',  datentyp='LongText')
        userdef1.add_daten_attribute('MATRIX', 'Category',  datentyp='LongText')

        netz = self.add_pgr_categories(vt, userdef1)

        model_code = 'VisemGGR'
        model_name = 'Visem Ziel- und Verkehrsmittelwahlmodell'
        self.add_demand_model(model_code, model_name, params.mode_set, vt)

        matrices = Matrix()

        self.add_params_persongrupmodel(userdef1)
        self.add_params_tripgeneration(userdef1)
        self.add_strukturgroessen(params.activities, model_code, vt)


        # Kenngrößenmatrizen
        matrices.set_category('General')
        matrices.add_daten_matrix('Diagonal',
                                  category='General',
                                  matrixtyp='Kenngröße',
                                  loadmatrix=1)
        matrices.add_daten_matrix('NoDiagonal',
                                  category='General',
                                  matrixtyp='Kenngröße',
                                  loadmatrix=1)
        matrices.add_ov_kg_matrices(params, userdef1, tag_index=tag_index)
        matrices.add_iv_kg_matrices(userdef1)

        acts = self.add_activities(userdef1, userdef2, matrices,
                                   params, model_code, vt)

        pg = self.add_persongroups(userdef1, userdef2, matrices, acts, netz,
                                   params, model_code, vt)

        ap = Aktivitaetenpaar()
        ap.create_tables(params.activitypairs, model=model_code)
        vt.tables['Aktivitaetenpaar'] = ap

        ak = Aktivitaetenkette()
        ak.create_tables(params.trip_chain_rates, model=model_code)
        vt.tables['Aktivitaetenkette'] = ak

        ns = Nachfrageschicht()
        userdef1.add_daten_attribute('Nachfrageschicht',
                                     'Mobilitaetsrate')
        userdef1.add_daten_attribute('Nachfrageschicht',
                                     'Tours',
                                     kommentar='Touren der Nachfrageschicht')
        userdef1.add_daten_attribute('Nachfrageschicht',
                                     'Trips',
                                     kommentar='Wege der Nachfrageschicht')
        userdef1.add_daten_attribute('Nachfrageschicht',
                                     'Tarifmatrix',
                                     datentyp='LongText',
                                     kommentar='Tarifmatrix der Nachfrageschicht')
        ns.create_tables_gd(personengruppe=pg,
                            aktivitaet=acts,
                            aktivitaetenkette=ak,
                            model=model_code,
                            category='ZielVMWahl')
        ns.create_tables_gd(personengruppe=pg,
                            aktivitaet=acts,
                            aktivitaetenkette=ak,
                            model=model_code,
                            category='ZielVMWahl_RSA')
        vt.tables['Nachfrageschicht'] = ns

        # Nachfragematrizen
        matrices.add_iv_demand(loadmatrix=1)
        matrices.add_ov_demand(loadmatrix=1)
        matrices.add_other_demand_matrices(params, loadmatrix=0)
        matrices.add_commuter_matrices(userdef1)

        # add matrices later
        vt.tables['Matrizen'] = matrices
        vt.tables['BenutzerdefinierteAttribute2'] = userdef2

        #  Skip adding logsum-Matrices
        if False:
            self.add_logsum_matrices(ak, ns, vt)

        self.add_ganglinien(pg, params, vt)

        fn = vt.get_modification(modification_number, self.modifications)
        vt.write(fn=fn)

    def add_logsum_matrices(self,
                            ak: Aktivitaetenkette,
                            ns: Nachfrageschicht,
                            vt: VisumTransfer):
        """Add logsum-matrices"""
        matrices_logsum = Matrix()
        matrices_logsum.add_logsum_matrices(ns, ak)
        vt.tables['MatrizenLogsum'] = matrices_logsum

    def add_ganglinien(self,
                       pg: Personengruppe,
                       params: Params,
                       vt: VisumTransfer):
        """Add the Ganglinien"""
        gl = Ganglinie()
        gle = Ganglinienelement()
        ngl = Nachfrageganglinie()
        vgl = VisemGanglinie()
        gl.create_tables(params.activitypairs,
                         params.time_series,
                         params.activitypair_time_series,
                         gle, ngl, vgl, pg)

        vt.tables['Ganglinie'] = gl
        vt.tables['Ganglinienelement'] = gle
        vt.tables['VisemGanglinien'] = vgl

    def add_persongroups(self,
                         userdef1: BenutzerdefiniertesAttribut,
                         userdef2: BenutzerdefiniertesAttribut,
                         matrices: Matrix,
                         acts: Aktivitaet,
                         netz: Netz,
                         params: Params,
                         model_code: str,
                         vt: VisumTransfer,
                         ) -> Personengruppe:
        """Create the Person Groups"""

        # add userdefined attributes for personsgroups
        pg = Personengruppe()
        pg._defaults['NACHFRAGEMODELLCODE'] = model_code
        vt.tables['PersonGroups'] = pg
        self.add_general_pgr_attributes(pg, userdef1, userdef2)

        modes = params.modes

        for _, mode in modes.iterrows():
            self.add_mode_specific_pgr_attributes(pg, mode, userdef1, userdef2)

        pg.add_df(params.group_definitions)
        # add the categories
        for pgr_category in params.group_definitions['CATEGORY'].unique():
            self.add_category(pgr_category, {}, netz)

        # create the groups for the RSA-Model
        categories = ['RSA', 'occupation', 'car_availability', 'Tarifzonen', 'Gesamt']
        category_generation = 'ErzeugungRSA'
        gg = pg.get_groups_destmode(categories, new_category=category_generation)
        pg.add_df(gg)

        category = 'ZielVMWahl_RSA'
        #tc_categories = ['occupation', 'car_availability']
        tc_categories = ['occupation']
        attrs = {
            'Comment': 'Zielwahl für Randsummenabgleich',
            'ActivityMatrixPrefix': 'Pendlermatrix_',
            'ActivityMatrixOBBPrefix': 'Pendlermatrix_OBB_',
            'Prefix_GG': 'RSA_',
            'PersonGroupPrefix': 'Pgr_',
            'RSA': True,
        }
        self.add_category(category, attrs, netz)
        pg.create_groups_destmode(params.groups_generation,
                                  params.trip_chain_rates_rsa,
                                  acts,
                                  model_code,
                                  tc_categories,
                                  category,
                                  category_generation,
                                  output_categories=['RSA'])

        #  Create the groups for the Main Model
        categories = ['occupation', 'car_availability', 'Tarifzonen', 'Gesamt']
        category_generation = 'Erzeugung'
        gg = pg.get_groups_destmode(categories, new_category=category_generation)
        pg.add_df(gg)

        category = 'ZielVMWahl'
        attrs = {
            'Comment': 'Ziel- und Verkehrsmittelwahl mit Visem',
            'ActivityMatrixPrefix': 'Activity_',
            'ActivityMatrixOBBPrefix': 'Activity_OBB_',
            'PersonGroupPrefix': 'Pgr_',
        }
        self.add_category(category, attrs, netz)
        tc_categories = ['occupation']
        pg.create_groups_destmode(params.groups_generation,
                                  params.trip_chain_rates,
                                  acts,
                                  model_code,
                                  tc_categories,
                                  category,
                                  category_generation,
                                  output_categories=categories)


        # Create the Dataframe
        pg.create_df_from_group_list()

        pg.add_calibration_matrices_and_attributes(modes, matrices)
        return pg

    def add_activities(self,
                       userdef1: BenutzerdefiniertesAttribut,
                       userdef2: BenutzerdefiniertesAttribut,
                       matrices: Matrix,
                       params: Params,
                       model_code: str,
                       vt: VisumTransfer,
                       ) -> Aktivitaet:
        """Add the activities and create the related tables"""
        # Aktivitäten
        acts = Aktivitaet()
        userdef1.add_daten_attribute('Aktivitaet', 'RSA', datentyp='Bool')
        userdef1.add_daten_attribute('Aktivitaet', 'Autocalibrate',
                                         datentyp='Bool')
        userdef1.add_daten_attribute('Aktivitaet', 'Composite_Activities',
                                         datentyp='Text')
        userdef1.add_daten_attribute('Aktivitaet', 'Aktivitaetset',
                                         datentyp='Text')
        userdef1.add_daten_attribute('Aktivitaet',
                                     code='CalcDestMode',
                                     name='CalculateDestinationAndModeChoice',
                                     datentyp='Bool')
        # spezifische Attribute für die Zielwahl
        userdef1.add_daten_attribute('Aktivitaet', 'LS',
                                     standardwert=1.0,
                                     kommentar='LogSum-Parameter der Aktivität, '
                                     'berechnet als Multiplikation der LS_Factors '
                                     'aller zugehörigen Aktivitäten')
        # spezifische Attribute für die Zielwahl
        userdef1.add_daten_attribute('Aktivitaet', 'BASE_LS',
                                     standardwert=1.0,
                                     kommentar='Basis-LogSum-Faktor der Aktivität, '
                                     'wird mit anderen Faktoren multipliziert')
        # spezifische Attribute für die Zielwahl
        userdef1.add_daten_attribute('Aktivitaet', 'KF_BASE_LS',
                                     standardwert=1.0,
                                     kommentar='Korrekturfaktor für LogSum der Aktivität, '
                                     'während Kalibrierung')
        # spezifische Attribute für die Verkehrsmittelwahl
        userdef1.add_daten_attribute(
            objid='AKTIVITAET',
            name='ZIELWAHL_FUNKTION_MATRIXCODES',
            datentyp='LongText',
            kommentar='Codes der Matrizen, die in die Zielwahl-Funktion einfliessen',
        )
        userdef1.add_daten_attribute(
            objid='AKTIVITAET',
            name='TARIFMATRIX',
            datentyp='LongText',
            kommentar='Name einer speziellen Tarifmatrix, '\
            'die bei dieser Hauptaktivität verwendet werden soll',
        )
        acts.create_tables(params.activities, model=model_code, suffix='')
        acts.add_benutzerdefinierte_attribute(userdef2)
        acts.add_net_activity_ticket_attributes(userdef2, params.modes)
        acts.add_output_matrices(matrices, userdef2)
        acts.add_modal_split(userdef2, matrices, params.modes)
        acts.add_balancing_output_matrices(matrices, userdef2, loadmatrix=0)
        acts.add_parking_matrices(matrices)
        acts.add_pjt_matrices(matrices)
        #acts.add_kf_logsum(userdef2)
        vt.tables['Aktivitaet'] = acts
        return acts

    def add_strukturgroessen(self,
                             activities: pd.DataFrame,
                             model_code: str,
                             vt: VisumTransfer):
        """Add Table Strukturgrößen"""
        sg = Strukturgr()
        sg.create_tables(activities, model=model_code, suffix='')
        vt.tables['Strukturgr'] = sg

    def add_demand_model(self,
                         model_code: str,
                         model_name: str,
                         mode_set: str,
                         v: VisumTransfer):
        """add the demand model with code and name and mode_set"""
        model = Nachfragemodell()
        row = model.Row(code=model_code,
                       name=model_name,
                       typ='VISEM',
                       modusset=mode_set)
        model.add_row(row)
        v.tables['Nachfragemodell'] = model

    def add_pgr_categories(self,
                           v: VisumTransfer,
                           userdef1: BenutzerdefiniertesAttribut) -> Netz:
        """Add userdefined net attribute"""
        netz = Netz(new_cols=['PgrCategories'])
        netz.add_rows([netz.Row()])
        v.tables['Netz'] = netz

        kommentar = 'Attribute der Personengruppen-Kategorien im json-Format'
        userdef1.add_daten_attribute('Netz',
                                         name='Persongroup_Categories',
                                         attid='PgrCategories',
                                         datentyp='LongText',
                                         maxstringlaenge=99999,
                                         kommentar=kommentar,
                                         )
        return netz


    def add_category(self,
                     category: str,
                     attrs: dict,
                     netz: Netz,
                     category_attribute: str = 'PgrCategories'):
        """
        Add category to the net-attribute category_attribute
        and set the attributes
        """
        categories = self.get_categories(netz)
        category_dict = categories.get(category, {})
        category_dict.update(attrs)
        categories[category] = category_dict
        netz.df.loc[0, category_attribute] = json.dumps(categories)

    def get_categories(self,
                       netz: Netz,
                       category_attribute='PgrCategories') -> dict:
        """Get the Categories from the category_attribute of the net"""
        categories_json = netz.df.loc[0, category_attribute]
        if not categories_json:
            return {}
        categories = json.loads(categories_json)
        return categories

    def add_general_pgr_attributes(self,
                                   pg: Personengruppe,
                                   userdef1: BenutzerdefiniertesAttribut,
                                   userdef2: BenutzerdefiniertesAttribut):
        """Add general Attributes for the Persongrups"""
        userdef1.add_daten_attribute('Personengruppe', 'CATEGORY', datentyp='Text',
                                         kommentar='Kategorie der Personengruppe')
        userdef1.add_daten_attribute(
            'Personengruppe', 'CODEPART', datentyp='Text',
            kommentar='Code-Bestandteil der Zusammengesetzten Personengruppen'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'NAMEPART', datentyp='Text',
            kommentar='Namens-Bestandteil der Zusammengesetzten Personengruppen'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'CALIBRATION_HIERARCHY', datentyp='Int',
            kommentar='Hierarchie bei der Kalibrierung des Modal Splits'
            'Der Modal Split der höchsten Hierarchiestufe wird zuletzt kalibriert'
            'und wird damit am genauesten getroffen.'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'ID_IN_CATEGORY', datentyp='Int',
            kommentar='Fortlaufende id innerhalb einer Kategorie')
        userdef1.add_daten_attribute(
            'Personengruppe', 'GROUPS_CONSTANTS', datentyp='Text',
            kommentar='Komma-getrennte Liste der Obergruppen, deren '
            'verkehrsmittelspezifische Konstante in die Nutzenfunktion einer '
            'Obergruppe einbezogen werden soll.'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'GROUPS_OUTPUT', datentyp='Text',
            kommentar='Komma-getrennte Liste der Obergruppen, in die die Berechnungs-'
            'Ergebnisse der Gruppe einfließen soll.'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'GROUP_GENERATION', datentyp='Text',
            kommentar='Code der Personengruppe für das Erzeugungsmodell'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'MAIN_ACT', datentyp='Text',
            kommentar='Hauptaktivität der Personengruppe'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'Persons', datentyp='Double',
            kommentar='Personen in Personengruppe'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'Faktor_Erwerbstaetigkeit', datentyp='Double',
            kommentar='Anteil der Erwerbstätigen an der Personengruppe',
        )
        userdef1.add_formel_attribute(
            'Personengruppe', 'Erwerbstaetige', datentyp='Double',
            formel='[PERSONS] * [FAKTOR_ERWERBSTAETIGKEIT]',
            kommentar='Erwerbstätige Personen',
        )
        userdef1.add_daten_attribute(
            'Personengruppe', 'Tarifmatrix', datentyp='LongText',
            kommentar='spezielle Tarifmatrix der Personengruppe',
        )
        pg.add_cols(['CATEGORY', 'CODEPART', 'NAMEPART',
                     'CALIBRATION_HIERARCHY', 'ID_IN_CATEGORY',
                     'GROUPS_CONSTANTS', 'GROUPS_OUTPUT', 'GROUP_GENERATION',
                     'MAIN_ACT', 'PERSONS', 'FAKTOR_ERWERBSTAETIGKEIT', 'TARIFMATRIX'])

        # Wege Gesamt und Verkehrsleistung der Gruppe
        formel = f'TableLookup(MATRIX Mat: Mat[CODE]="Pgr_"+[CODE]: Mat[SUMME])'
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Trips',
            formel=formel,
            kommentar=f'Gesamtzahl der Wege der Gruppe',
        )
        formel = f'TableLookup(MATRIX Mat: Mat[CODE]="VL_Pgr_"+[CODE]: Mat[SUMME])'
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Km',
            formel=formel,
            kommentar=f'Gesamte Verkehrsleistung der Gruppe',
        )
        # Mittlere Wegelänge
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'MeanTripLength',
            formel='[Km]/[Trips]',
            kommentar=f'Mittlere Wegelänge [km]',
        )
        # Wege und Verkehrsleistung pro Person
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Trips_per_Person',
            formel='[Trips]/[Persons]',
            kommentar=f'Wege Pro Person',
        )
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Km_per_Person',
            formel='[Km]/[Persons]',
            kommentar=f'Wege Pro Person',
        )

    def add_mode_specific_pgr_attributes(self,
                                         pg: Personengruppe,
                                         mode: pd.Series,
                                         userdef1: BenutzerdefiniertesAttribut,
                                         userdef2: BenutzerdefiniertesAttribut):
        """Add mode-specific Attributes for the Persongrups"""
        m = mode.code
        userdef1.add_daten_attribute(
            'Personengruppe', f'BASECONST_{m}', datentyp='Double',
            kommentar=f'Konstante für Verkehrsmittel {mode.name}'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', f'CONST_{m}', datentyp='Double',
            kommentar=f'Konstante für Verkehrsmittel {mode.name}'
        )
        userdef1.add_daten_attribute(
            'Personengruppe', f'TARGET_MS_{m}', datentyp='Double',
            kommentar=f'Ziel-ModalSplit für Verkehrsmittel {mode.name}'
        )
        userdef1.add_daten_attribute(
            objid='PERSONENGRUPPE',
            name=f'KF_CONST_{m}',
            standardwert=0,
            kommentar=f'Korrektur der Konstante bei Kalibrierung für {mode.name}',
        )

        pg.add_cols([f'BASECONST_{m}', f'CONST_{m}', f'TARGET_MS_{m}', f'KF_CONST_{m}'])

        # Wege nach Modus und Modal Split der Gruppe
        formel = f'TableLookup(MATRIX Mat: Mat[CODE]="Pgr_"+[CODE]+"_{m}": Mat[SUMME])'
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Trips_{m}',
            formel=formel,
            kommentar=f'Gesamtzahl der Wege mit Verkehrsmittel {mode.name}',
        )
        formel = f'TableLookup(MATRIX Mat: Mat[CODE]="VL_Pgr_"+[CODE]+"_{m}": Mat[SUMME])'
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Km_{m}',
            formel=formel,
            kommentar=f'Verkehrsleistung mit Verkehrsmittel {mode.name} der Gruppe',
        )
        # Modal Split der Gruppe
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'MS_{m}',
            formel=f'[Trips_{m}] / [Trips]',
            kommentar=f'Modal Split-Anteil {mode.name}',
        )
        # Mittlere Wegelänge
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'MeanTripLength_{m}',
            formel=f'[Km_{m}]/[Trips_{m}]',
            kommentar=f'Mittlere Wegelänge {mode.name}',
        )
        # Wege und Verkehrsleistung pro Person
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Trips_Per_Person_{m}',
            formel=f'[Trips_{m}] / [Persons]',
            kommentar=f'Modal Split-Anteil {mode.name}',
        )
        userdef2.add_formel_attribute(
            objid='PERSONENGRUPPE',
            name=f'Km_Per_Person_{m}',
            formel=f'[Km_{m}] / [Persons]',
            kommentar=f'Km pro Person {mode.name}',
        )

    def add_params_persongrupmodel(self, userdef1: BenutzerdefiniertesAttribut):
        params_pgrmodel = dict(
            excel_filename="ParamsPersongroupModel.xlsx",
            excel_folder='',
            sn_occupation='Taetigkeit_Long',
            sn_caravailability='Pkwverf_Long',
            sn_lab_occupation='lab_taetigkeit',
            sn_lab_caravailability='lab_pkwverf',
            sn_lab_gebiet='lab_gebiet',
        )
        userdef1.add_daten_attribute(
            'Netz',
            'ParamFilePersongroupModel',
            datentyp='LongText',
            maxstringlaenge=99999,
            stringstandardwert=json.dumps(params_pgrmodel))

        # Attribute für Motorisierung
        userdef1.add_daten_attribute('Bezirk', 'Pkw_Personengruppen')        formel = '[Pkw_Personengruppen] / [ANZPERSONEN(XSumme)] * 1000'
        userdef1.add_formel_attribute('Bezirk', 'Motorisierung', formel=formel)        userdef1.add_daten_attribute('Netz', 'Pkw_per_CarAvailabilityGroup')
        kommentar = 'Pkw nach Pkw-Verfügbarkeit im json-Format'
        userdef1.add_daten_attribute('Netz',
                                     name='Pkw nach PkwVerfügbarkeit',
                                     attid='Cars_By_Caravailability',
                                     datentyp='LongText',
                                     maxstringlaenge=99999,
                                     kommentar=kommentar,
                                     )

    def add_params_tripgeneration(self, userdef1: BenutzerdefiniertesAttribut):
        params_tcr = dict(
            excel_filename="params_long_2020.xlsx",
            excel_folder='',
            sn_trc='trip_chain_rates',
        )
        userdef1.add_daten_attribute(
            'Netz',
            'ParamFileTripGenerationModel',
            datentyp='LongText',
            maxstringlaenge=99999,
            stringstandardwert=json.dumps(params_tcr))

    def write_modification_iv_matrices(self, modification_number: int):
        v = VisumTransfer.new_transfer()

        matrices = Matrix()
        matrices.add_iv_demand()
        v.tables['Matrizen'] = matrices
        v.write(fn=v.get_modification(modification_number, self.modifications))


    def write_modification_ov_matrices(self, modification_number: int):
        v = VisumTransfer.new_transfer()

        matrices = Matrix()
        matrices.add_ov_demand()
        v.tables['Matrizen'] = matrices
        v.write(fn=v.get_modification(self.modifications, modification_number))


    def add_nsegs_userdefined(self, modification_no: int):
        vt = VisumTransfer.new_transfer()
        userdef0 = BenutzerdefiniertesAttribut()
        vt.tables['BenutzerdefinierteAttribute0'] = userdef0

        # Matrizen
        userdef0.add_daten_attribute('Matrix', 'INITMATRIX', datentyp='Bool')
        userdef0.add_daten_attribute('Matrix', 'LOADMATRIX', datentyp='Bool')
        userdef0.add_daten_attribute('Matrix', 'SAVEMATRIX', datentyp='Bool')
        userdef0.add_daten_attribute('Matrix', 'MATRIXFOLDER', datentyp='Text')
        userdef0.add_daten_attribute('Matrix', 'CALIBRATIONCODE', datentyp='Text')
        userdef0.add_daten_attribute('Matrix', 'CATEGORY', datentyp='Text')

        # Netzattribute
        userdef0.add_daten_attribute('Netz', 'COST_PER_KM_PKW',
                                         standardwert=0.15)
        userdef0.add_daten_attribute('Netz', 'MINUS_ONE', standardwert=-1)

        mode_lkw = 'X'
        # Nachfragesegmente
        nseg = Nachfragesegment()
        vt.tables['Nachfragesegment'] = nseg
        #nseg.add_row(nseg.Row(code='O', name='ÖV Region', modus='O'))
        #nseg.add_row(nseg.Row(code='OFern', name='ÖV Fernverkehr', modus='O'))
        #nseg.add_row(nseg.Row(code='B_P', name='Pkw-Wirtschaftsverkehr',
                              #modus='P'))
        #nseg.add_row(nseg.Row(code='B_Li', name='Lieferfahrzeug',
                              #modus='P'))
        #nseg.add_row(nseg.Row(code='B_L1', name='Lkw bis 12 to',
                              #modus=mode_lkw))
        #nseg.add_row(nseg.Row(code='B_L2', name='Lkw 12-40 to',
                              #modus=mode_lkw))
        #nseg.add_row(nseg.Row(code='LkwFern', name='Lkw Fernverkehr',
                              #modus=mode_lkw))
        #nseg.add_row(nseg.Row(code='PkwFern', name='Pkw Fernverkehr',
                              #modus='P'))
        nseg.add_row(nseg.Row(code='SV', name='Schwerverkehr',
                              modus=mode_lkw))
        nseg.add_row(nseg.Row(code='PG', name='Kfz bis 3,5 to',
                              modus='P'))

        fn = vt.get_modification(modification_no, self.modifications)
        vt.write(fn=fn)

    def create_transfer_target_values(self, params: Params, modification_no: int):

        cols = [f'TARGET_MS_{mode.code}' for _, mode in params.modes.iterrows()]
        v = VisumTransfer.new_transfer()

        # Personengruppenspezifische Zielwerte Modal Split
        gd = params.group_definitions.set_index('CODE')
        gd = gd[cols]
        gd = gd.loc[gd.any(axis=1)]
        pg = Personengruppe(mode='*')
        pg.df = gd
        v.tables['Personengruppe'] = pg

        # Aktivitätenspezifische Zielwerte Modal Split
        va = params.validation_activities.set_index('code')
        va = va.loc[va['in_model'] == 1]
        va = va[cols + ['Target_MeanTripDistance']]
        va = va.loc[va.any(axis=1)]
        ac = Aktivitaet(mode='*')
        ac.df = va
        v.tables['Aktivitaet'] = ac

        #  Zielwerte Mittlere Wegelängen Aktivitäten

        fn = v.get_modification(modification_no, self.modifications)
        v.write(fn=fn)


    def create_transfer_constants(self, params: Params, modification_no: int):
        cols = [f'BASECONST_{mode.code}' for _, mode in params.modes.iterrows()]

        v = VisumTransfer.new_transfer()

        # Personengruppenspezifische Konstanten
        gd = params.group_definitions.set_index('CODE')
        gd = gd[cols]
        gd = gd.loc[gd.any(axis=1)]
        pg = Personengruppe(mode='*')
        pg.df = gd
        v.tables['Personengruppe'] = pg

        # Aktivitätenspezifische Konstanten
        va = params.validation_activities.set_index('code')
        va = va.loc[va['in_model']==1]
        va = va[cols]
        va = va.loc[va.any(axis=1)]
        ac = Aktivitaet(mode='*')
        ac.df = va
        v.tables['Aktivitaet'] = ac

        #  Logsum-Parameter
        acts = params.activities.set_index('code')
        acts = acts[['BASE_LS']]
        acts = acts.loc[acts.any(axis=1)]
        ac_ls = Aktivitaet(mode='*')
        ac_ls.df = acts
        v.tables['Aktivitaet_Logsum'] = ac_ls

        fn = v.get_modification(modification_no, self.modifications)
        v.write(fn=fn)

    def get_params(self, param_excel_fp: str) -> Params:
        return Params(param_excel_fp)


if __name__ == '__main__':
    argpase = ArgumentParser()
    argpase.add_argument('--infolder', type=str)
    argpase.add_argument('--param_excel_fp', type=str, default='tdm_params.xlsx')
    argpase.add_argument('--visum_folder', type=str, default='D:\GGR\H\VISH-VEP19')
    options = argpase.parse_args()

    param_excel_fp = os.path.join(options.infolder, options.param_excel_fp)
    modifications = os.path.join(options.visum_folder, 'Modifications')
    shared_data = os.path.join(options.visum_folder, 'SharedData')

    dm = VisemDemandModel(modifications,
                          param_excel_fp,
                          )

    params = dm.get_params(param_excel_fp)
    #dm.add_nsegs_userdefined(modification_no=444)
    dm.create_transfer(params, modification_number=16, tag_index=318)
    #dm.create_transfer_constants(params, modification_no=17)
    #dm.create_transfer_target_values(params, modification_no=18)
    # dm.write_modification_iv_matrices(modification_no=12)
    #dm.write_modification_ov_matrices(modification_no=14)
