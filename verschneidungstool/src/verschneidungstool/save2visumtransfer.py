import pandas as pd
from visumtransfer.visum_table import VisumTransfer, VisumTable
from visumtransfer.visum_tables import (BenutzerdefinierteGruppe,
                                        BenutzerdefiniertesAttribut,
                                        Bezirke,
                                        Oberbezirk,
                                        Gebiete,
                                        Strukturgroessenwert,
                                        PersonengruppeJeBezirk,
                                        )


def save_to_visum_transfer(df: pd.DataFrame,
                           filepath: str,
                           category: str,
                           visum_classname: str = 'Bezirke',
                           append: bool = False,
                           long_format: bool=False):
    """
    write the Dataframe df to the transfer-file in the section for the Visum-Table
    defined by the visum_classname
    if append, append the table to the transfer-file, if not, create a new
    transfer-file with a VERSION-section

    if long_format is specified, assume, that the data from the Dataframe is
    already in long-format. If not, convert wide to long for PersonengruppeJeBezirk
    and Strukturgroessenwert
    """
    Level: VisumTable = globals().get(visum_classname)
    if not Level:
        raise ValueError(f'{visum_classname} not defined or imported')
    assert issubclass(Level, VisumTable), f'{visum_classname} is not a subclass of VisumTable'

    transfer = VisumTransfer.new_transfer()

    if Level._longformat:
        if not long_format:
            df2 = pd.wide_to_long(df.reset_index(),
                                  '#', 'vz_id', 'STRUKTURGROESSENCODE',
                                  suffix='[\w\W]+').reset_index()
        else:
            df2 = df.reset_index()
        visum_table = Level(mode='')
        df2.columns = visum_table.cols
        #  select the rows where the value (in the last column) is greater than 0
        df_gt0 = df2.loc[df2.iloc[:, -1] > 0]
        visum_table.df = df_gt0
        transfer.add_table(visum_table)

    else:
        userdefined = BenutzerdefiniertesAttribut(mode='')
        zones = Level(mode='*')
        dtype2datatype = {'f': 'Double',
                          'i': 'Int',
                          'O': 'Text',
                          'b': 'Bool', }

        for colname in df.columns:
            col = df[colname]
            datatype = dtype2datatype.get(col.dtype.kind, 'Double')
            userdefined.add_daten_attribute(Level.code,
                                            colname,
                                            datentyp=datatype,
                                            benutzerdefiniertergruppenname=category)

        df.index.name = zones.pkey[0]
        zones.df = df

        transfer.add_table(userdefined)
        transfer.add_table(zones)
    if append:
        transfer.append(filepath)
    else:
        transfer.write(filepath)


def prepend_categories(filepath: str, categories: set):
    """Prepend userdefined groups to transfer file"""
    transfer = VisumTransfer.new_transfer()
    userdefgroups = BenutzerdefinierteGruppe(mode='+')
    transfer.add_table(userdefgroups)

    for category in categories:
        userdefgroups.upsert(name=category)

    transfer.prepend(filepath)
