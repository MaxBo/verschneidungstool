import pandas as pd
from visumtransfer.visum_table import VisumTransfer
from visumtransfer.visum_demand import BenutzerdefiniertesAttribut, Bezirke


def save_to_visum_transfer(df: pd.DataFrame,
                           filepath: str):
    userdefined = BenutzerdefiniertesAttribut(mode='+')
    zones = Bezirke(mode='*')
    dtype2datatype = {'d': 'Double',
                      'O': 'String', }

    for colname in df.columns:
        col = df[colname]
        datatype = dtype2datatype.get(col.dtype.char, 'Double')
        userdefined.add_daten_attribute('BEZIRK', colname, datentyp=datatype)

    zones.df = df

    transfer = VisumTransfer.new_transfer()
    transfer.add_table(userdefined)
    transfer.add_table(zones)
    transfer.write(filepath)

