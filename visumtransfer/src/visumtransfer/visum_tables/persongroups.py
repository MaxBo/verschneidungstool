# -*- coding: utf-8 -*-

from typing import List
import pandas as pd
from collections import defaultdict
from .matrizen import Matrix
from .activities import Aktivitaet
from visumtransfer.visum_table import VisumTable


class Personengruppe(VisumTable):
    name = 'Personengruppen'
    code = 'PERSONENGRUPPE'
    _cols = 'CODE;NAME;NACHFRAGEMODELLCODE'

    def __init__(self, mode='+'):
        super().__init__(mode=mode)
        self.groups = []
        self.gd_codes = defaultdict(list)

    def add_group(self, code: str, model_code: str, **kwargs):
        row = self.Row(code=code,
                       nachfragemodellcode=model_code,
                       **kwargs)
        self.groups.append(row)

    def get_groups_destmode(self,
                            categories: List[str],
                            new_category: str) -> pd.DataFrame:
        """Create Groups as combinations of the categories"""
        assert categories, f'you need at least one category'

        # take the first category
        category = categories[0]
        df = self.df.reset_index()
        df = df.loc[df['CATEGORY'] == category,
                    ['CODE', 'NAME', 'NAMEPART', 'GROUPS_CONSTANTS', 'CODEPART']]
        df['GROUPS_CONSTANTS'] = df['CODE']
        df['CODE'] = df['CODEPART']
        df['NAME'] = df['NAMEPART']
        df.drop(['CODEPART', 'NAMEPART'], axis=1, inplace=True)
        assert len(df), f'no groups defined for category {category}'

        # cross join with the other categories
        for category in categories[1:]:
            df_new = self.df.reset_index()
            df_cat = df_new.loc[df_new['CATEGORY'] == category,
                                ['CODE', 'NAMEPART', 'CODEPART']]\
                .rename(columns={'CODE': 'CODE_new'})\
                .assign(one=1)
            assert len(df_cat), f'no groups defined for category {category}'

            df = df.assign(one=1).merge(df_cat, on='one').drop('one', 1)

            # define code, name and groups_const for composite groups
            df['CODE'] = df['CODE'] + df['CODEPART']
            new_name = df['NAME'] + ', ' + df['NAMEPART']
            df['NAME'] = new_name.str.strip(', ')
            new_groups_constants = df['GROUPS_CONSTANTS'] + ',' + df['CODE_new']
            df['GROUPS_CONSTANTS'] = new_groups_constants
            df.drop(['CODE_new', 'CODEPART', 'NAMEPART'], axis=1, inplace=True)

        df['CATEGORY'] = new_category
        return df

    def create_groups_destmode(self,
                               groups_generation: pd.DataFrame,
                               trip_chain_rates: pd.DataFrame,
                               activities: Aktivitaet,
                               model_code: str,
                               tc_categories: List[str],
                               category: str,
                               category_generation: str,
                               output_categories: List[str] = [],
                               ):
        """Create the Groups for the Destination and Model modelling"""
        pgr_in_categories = self.df.loc[self.df['CATEGORY'].isin(tc_categories)].index
        pgr_in_output_categories = self.df.loc[self.df['CATEGORY'].isin(
            output_categories)].index

        pgr_generation = self.df.loc[self.df['CATEGORY'] == category_generation].copy()

        # create common column to merge Persongrups and TripChainRates
        pgr_generation['gr_tc'] = ''
        for pg_code, gr_const in pgr_generation['GROUPS_CONSTANTS'].iteritems():
            gr_split = gr_const.split(',')
            gr_tc = ','.join(sorted([gr
                                     for gr in gr_split
                                     if gr in pgr_in_categories]))
            pgr_generation.loc[pg_code, 'gr_tc'] = gr_tc

        pgr_generation.index.name = 'PGRCODES'

        trip_chain_rates['gr_tc'] = ''
        for idx, gr_const in trip_chain_rates['group_generation'].iteritems():
            gr_split = gr_const.split(',')
            gr_tc = ','.join(sorted([gr for gr in gr_split]))
            trip_chain_rates.loc[idx, 'gr_tc'] = gr_tc

        trip_chain_rates.rename(columns={'code': 'code_tc',}, inplace=True)
        tcs = pgr_generation.reset_index().merge(trip_chain_rates, on='gr_tc')
        assert len(tcs), f'No matching tripchains found for categories {tc_categories}'

        act_hierarchy = activities.get_hierarchy()

        # loop over all tripchains in the groups
        for _, tc in tcs.iterrows():
            gg_code = tc['PGRCODES']
            gd_code = tc['PGRCODES']
            act_code = tc['code_tc']
            act_sequence = tc['Sequence']
            tc_name = tc['NAME']
            mobilitaetsrate = tc['rate']
            main_act = activities.get_main_activity(act_hierarchy, act_sequence)
            code = '_'.join((gd_code, main_act))
            # if the the group occurs the first time ...
            if code not in self.gd_codes:
                #  create it and add it to self.gd_codes
                self.gd_codes[code] = [(act_code, mobilitaetsrate)]
                name = f'{tc_name} mit Hauptaktivität {main_act}'
                groups_constants = tc['GROUPS_CONSTANTS']
                gr_split = groups_constants.split(',')
                groups_output = [gr
                                 for gr in gr_split
                                 if gr in pgr_in_output_categories]
                grcodes_output = ','.join(groups_output)

                self.add_group(
                    category=category,
                    model_code=model_code,
                    code=code,
                    name=name,
                    groups_constants=groups_constants,
                    groups_output=grcodes_output,
                    group_generation=gg_code,
                    main_act=main_act)
            else:
                # otherwise just append the activity chain
                # to the chains the persons makes
                self.gd_codes[code].append((act_code, mobilitaetsrate))

    def create_df_from_group_list(self):
        df = self.df_from_array(self.groups)
        self.add_df(df)

    def add_calibration_matrices_and_attributes(
            self,
            modes: pd.DataFrame,
            matrices: Matrix):
        """
        Add Output Matrices for PersonGroups
        """
        matrices.set_category('Demand_Pgr')
        df_groups_output = self.df['GROUPS_OUTPUT'].str.split(',', expand=True)
        df_groups_output.columns = [f'group{i}'
                                    for i in df_groups_output.columns]
        df_out_long = pd.wide_to_long(df_groups_output.reset_index(),
                                      'group',
                                      'CODE',
                                      'gr_id')
        df_out_long = df_out_long.loc[~df_out_long['group'].isnull()]
        df_out_long.set_index(df_out_long.index.droplevel(level=1), inplace=True)
        prefix = 'Pgr_'

        for group_output, detailed_groups in df_out_long.groupby(by='group'):
            gr = self.df.loc[group_output]
            str_name = f'Wege der {gr.CATEGORY}-Gruppe {gr.NAME}'
            code = f'{prefix}{gr.name}'
            pgrset = ','.join(detailed_groups.index)
            matrices.add_daten_matrix(
                code=code,
                name=str_name,
                modusset=','.join(modes['code']),
                personengruppenset=pgrset,
                pgruppencode=group_output,
            )
            vl_code = f'VL_{code}'
            formel_vl = f'Matrix([CODE]="{code}") * Matrix([CODE]="KM")'
            vl_name = f'Verkehrsleistung der {gr.CATEGORY}-Gruppe {gr.NAME}'

            matrices.add_formel_matrix(
                code=vl_code,
                formel=formel_vl,
                name=vl_name,
                modusset=','.join(modes['code']),
                personengruppenset=pgrset,
                pgruppencode=group_output,
            )

            for _, mode in modes.iterrows():
                mode_name = mode['name']
                # add output matrix
                str_name = f'Wege mit Verkehrsmittel {mode_name} der {gr.CATEGORY}-Gruppe {gr.NAME}'
                code = f'{prefix}{gr.name}_{mode.code}'
                pgrset = ','.join(detailed_groups.index)
                matrices.add_daten_matrix(
                    code=code,
                    name=str_name,
                    moduscode=mode.code,
                    modusset=mode.code,
                    personengruppenset=pgrset,
                    pgruppencode=group_output,
                )
                vl_code = f'VL_{code}'
                formel_vl = f'Matrix([CODE]="{code}") * Matrix([CODE]="KM")'
                vl_name = f'Verkehrsleistung mit Verkehrsmittel {mode_name} der {gr.CATEGORY}-Gruppe {gr.NAME}'
                matrices.add_formel_matrix(
                    code=vl_code,
                    formel=formel_vl,
                    name=vl_name,
                    modusset=','.join(modes['code']),
                    personengruppenset=pgrset,
                    pgruppencode=group_output,
                )
