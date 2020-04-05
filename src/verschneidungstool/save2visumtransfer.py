import pandas as pd
from visumtransfer.visum_table import VisumTransfer, VisumTable
from visumtransfer.visum_demand import (BenutzerdefiniertesAttribut,
                                        Bezirke,
                                        Oberbezirk)


def save_to_visum_transfer(df: pd.DataFrame,
                           filepath: str,
                           visum_classname: str = 'Bezirke',
                           append: bool = False):
    Level = globals().get(visum_classname)
    if not Level:
        raise ValueError(f'{visum_classname} not defined or imported')
    assert issubclass(Level, VisumTable), f'{visum_classname} is not a subclass of VisumTable'
    userdefined = BenutzerdefiniertesAttribut(mode='+')
    zones = Level(mode='*')
    dtype2datatype = {'f': 'Double',
                      'i': 'Int',
                      'O': 'Text',
                      'b': 'Bool',}

    for colname in df.columns:
        col = df[colname]
        datatype = dtype2datatype.get(col.dtype.kind, 'Double')
        userdefined.add_daten_attribute(Level.code, colname, datentyp=datatype)

    df.index.name = zones.pkey
    zones.df = df

    transfer = VisumTransfer.new_transfer()
    transfer.add_table(userdefined)
    transfer.add_table(zones)
    if append:
        transfer.append(filepath)
    else:
        transfer.write(filepath)

