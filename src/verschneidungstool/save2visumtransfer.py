import pandas as pd
from visumtransfer.visum_table import VisumTransfer, VisumTable
from visumtransfer.visum_tables import (BenutzerdefiniertesAttribut,
                                        Bezirke,
                                        Oberbezirk,
                                        Gebiete,
                                        Strukturgroessenwert,
                                        PersonengruppeJeBezirk,
                                        )


def save_to_visum_transfer(df: pd.DataFrame,
                           filepath: str,
                           visum_classname: str = 'Bezirke',
                           append: bool = False):
    Level: VisumTable = globals().get(visum_classname)
    if not Level:
        raise ValueError(f'{visum_classname} not defined or imported')
    assert issubclass(Level, VisumTable), f'{visum_classname} is not a subclass of VisumTable'

    transfer = VisumTransfer.new_transfer()

    if Level._longformat:
        df2 = pd.wide_to_long(df.reset_index(),
                              '#', 'vz_id', 'STRUKTURGROESSENCODE',
                              suffix='\w+').reset_index()
        visum_table = Level(mode='')
        df2.columns = visum_table.cols
        #  select the rows where the value (in the last column) is greater than 0
        df_gt0 = df2.loc[df2.iloc[:, -1] > 0]
        visum_table.df = df_gt0
        transfer.add_table(visum_table)

    else:
        userdefined = BenutzerdefiniertesAttribut(mode='+')
        zones = Level(mode='*')
        dtype2datatype = {'f': 'Double',
                          'i': 'Int',
                          'O': 'Text',
                          'b': 'Bool', }

        for colname in df.columns:
            col = df[colname]
            datatype = dtype2datatype.get(col.dtype.kind, 'Double')
            userdefined.add_daten_attribute(Level.code, colname, datentyp=datatype)

        df.index.name = zones.pkey
        zones.df = df

        transfer.add_table(userdefined)
        transfer.add_table(zones)
    if append:
        transfer.append(filepath)
    else:
        transfer.write(filepath)

