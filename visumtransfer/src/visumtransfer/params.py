import json
import pandas as pd
import openpyxl
from typing import List


class Params:
    modes: pd.DataFrame
    group_definitions: pd.DataFrame
    groups_generation: pd.DataFrame
    activities: pd.DataFrame
    activity_parking: pd.DataFrame
    activitypairs: pd.DataFrame
    activitypair_time_series: pd.DataFrame
    time_series: pd.DataFrame
    trip_chain_rates: pd.DataFrame
    validation_activities: pd.DataFrame
    validation_activities_hauptweg: pd.DataFrame
    trip_chain_rates_rsa: pd.DataFrame
    """"""
    attr2tablename = dict(
        group_definitions='group_definitions',
        groups_generation='groups_generation',
        activities='activities',
        activity_parking='activity_parking',
        activitypairs='activitypairs',
        activitypair_time_series='activitypair_time_series',
        time_series='time_series',
        trip_chain_rates='trip_chain_rates',
        validation_activities='validation_activities',
        validation_activities_hauptweg='validation_hauptweg',
        modes='modes',
        trip_chain_rates_rsa='trip_chain_rates_rsa',
    )

    def __init__(self, excel_fp: str):
        """ Read tables from """
        self.dataframes = {}
        with pd.ExcelFile(excel_fp) as excel:

            for k, v in self.attr2tablename.items():
                #  excel-sheetnames may be only 30 letters long
                sheet_name = v[:30]
                df = pd.read_excel(excel, sheet_name,
                                   keep_default_na=False)
                for colname in df.columns:
                    try:
                        converted = pd.to_numeric(df[colname])
                        df.loc[:, colname] = converted
                    except ValueError:
                        pass
                self.dataframes[k] = df
                setattr(self, k, df)

    @property
    def mode_set(self) -> str:
        modes = self.modes['code']
        return ','.join(modes)

    def save2excel(self, excel_fp: str, keys: List = None):
        """Save parameters in different excel sheets"""
        with pd.ExcelWriter(excel_fp, engine='openpyxl') as excel:
            try:
                excel.book = openpyxl.load_workbook(excel_fp)
            except FileNotFoundError:
                pass
            for k, v in self.attr2tablename.items():
                if keys is None or k in keys:
                    df = getattr(self, k)
                    for col_name in df.columns:
                        col = df[col_name]
                        if col.dtype.char == 'O' and isinstance(col[0], bytes):
                            df[col_name] = col.str.decode('cp1252')

                    sheet_name = v.replace('.', '_')[:30]
                    try:
                        old_sheet = excel.book.get_sheet_by_name(sheet_name)
                        excel.book.remove_sheet(old_sheet)
                    except KeyError:
                        pass
                    df.to_excel(excel, sheet_name=sheet_name)

    def __repr__(self) -> str:
        tbls = json.dumps(self.attr2tablename, indent=2)
        #return tbls
        return f'Params-object with the following tables: {tbls}'

