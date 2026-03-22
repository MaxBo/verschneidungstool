import pandas as pd
from visumtransfer.visum_table import VisumTransfer, VisumTable
import visumtransfer.visum_tables
from visumtransfer.visum_tables import (UserDefinedGroup,
                                        UserDefinedAttribute,
                                        )


def save_to_visum_transfer(df: pd.DataFrame,
                           filepath: str,
                           category: str,
                           visum_classname: str = 'Zone',
                           append: bool = False,
                           long_format: bool=False):
    """
    write the Dataframe df to the transfer-file in the section for the Visum-Table
    defined by the visum_classname
    if append, append the table to the transfer-file, if not, create a new
    transfer-file with a VERSION-section

    if long_format is specified, assume, that the data from the Dataframe is
    already in long-format. If not, convert wide to long for PersonGroupPerZone
    and StructuralPropValues
    """
    Level: VisumTable = getattr(visumtransfer.visum_tables, visum_classname, None)
    if not Level:
        raise ValueError(f'{visum_classname} not defined in {visumtransfer.visum_tables.__file__}')
    assert issubclass(Level, VisumTable), f'{visum_classname} is not a subclass of VisumTable'

    transfer = VisumTransfer.new_transfer()

    if Level._longformat:
        if not long_format:
            df2 = pd.wide_to_long(df.reset_index(),
                                  '#', 'vz_id', 'STRUKTURGROESSENCODE',
                                  suffix=r'[\w\W]+').reset_index()
        else:
            df2 = df.reset_index()
        visum_table = Level(mode='')
        df2.columns = visum_table.cols
        #  select the rows where the value (in the last column) is greater than 0
        df_gt0 = df2.loc[df2.iloc[:, -1] > 0]
        visum_table.df = df_gt0
        transfer.add_table(visum_table)

    else:
        userdefined = UserDefinedAttribute(mode='')
        zones = Level(mode='*')
        dtype2datatype = {'f': 'Double',
                          'i': 'Int',
                          'O': 'Text',
                          'b': 'Bool', }

        for colname in df.columns:
            if zones.column_exists(colname):
                continue
            col = df[colname]
            valuetype = dtype2datatype.get(col.dtype.kind, 'Double')
            userdefined.add_data_attribute(Level.code,
                                            colname,
                                            valuetype=valuetype,
                                            userdefinedgroupname=category)

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
    userdefgroups = UserDefinedGroup(mode='')
    transfer.add_table(userdefgroups)

    for category in categories:
        userdefgroups.upsert(name=category)

    transfer.prepend(filepath)
