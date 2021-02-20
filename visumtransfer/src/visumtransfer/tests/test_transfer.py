import os
import pytest
import numpy as np
import pandas as pd
from visumtransfer.visum_table import (VisumTable, VisumTables,
                                       Version)
from visumtransfer.visum_attributes import VisumAttributes


@pytest.fixture
def dataframe() -> pd.DataFrame:
    df = pd.DataFrame(data=np.array([(2, 'A', 33.3),
                                     (4, 'B', 44.4)]),
                      columns=['ID', 'NAME', 'Value'])
    return df


@pytest.fixture(scope='function')
def visum_tables():
    tables = VisumTables()
    return tables


@pytest.fixture
def visum_attribute_file() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'attributes.h5')


class DummyTable(VisumTable):
    name = 'Dummies'
    code = 'DUMMY'
    _cols = 'ID;NAME;VALUE'
    _pkey = 'ID'
    _defaults = {'VALUE': -11, }


class TestVisumTableCreation:
    def test_findVisumTable(self, visum_tables):
        """Test if the VisumTable ist found"""
        # test if table defined in other module is recognized
        assert 'VERSION' in visum_tables.tables
        assert visum_tables.tables['VERSION'] == Version
        # test if table defined in this module is recognized
        assert 'DUMMY' in visum_tables.tables
        assert visum_tables.tables['DUMMY'] == DummyTable


class TestVisumAttributes:
    """test the visum attributes"""
    @pytest.mark.skip(msg="attributes are normally already converted")
    def test_convert_attributes(self, visum_attribute_file):
        visum_attributes = VisumAttributes(visum_attribute_file)

    def test_get_attribute(self, visum_attribute_file):
        visum_attributes = VisumAttributes.from_hdf(visum_attribute_file)
        tables = visum_attributes.tables.reset_index().set_index('Long(DEU)')
        row = tables.loc['Bezirke']
        assert row.Name == 'Zone'


class TestVisumTransfer:
    """"""
    def test_add_rows(self, dataframe):
        """test adding rows to the DataFrame"""
        tbl = DummyTable(mode='+')
        new_row = tbl.Row(id=2)
        assert new_row.value == DummyTable._defaults['VALUE']
        assert new_row.id == 2
        new_row.name = 'ABC'
        assert new_row.name == 'ABC'

        tbl.add_row(new_row)
        assert len(tbl) == 1
        self.assert_row_equals(tbl, new_row)

        new_row = tbl.Row(id=3, name='DDD')

        tbl.add_row(new_row)
        assert len(tbl) == 2
        self.assert_row_equals(tbl, new_row)

        #  duplicate primary key should raise a ValueError
        new_row = tbl.Row(id=2, name='EEE')
        with pytest.raises(ValueError,
                           match=r'Indexes have overlapping values'):
            tbl.add_row(new_row)
        assert len(tbl) == 2

        #  test adding five more rows with ids 10-14
        new_rows = [tbl.Row(id=n) for n in range(10, 15)]
        tbl.add_rows(new_rows)
        assert len(tbl) == 7
        # the penultimate should have the no 13
        self.assert_row_equals(tbl, tbl.Row(id=13), -2, )

    def assert_row_equals(self,
                          table: VisumTable,
                          row: 'VisumTable.Row',
                          rowno: int = - 1, ):
        """
        compare the nth row in the dataframe to the row

        Parameters
        ----------
        rowno : int, optional (Default=-1)
            then row number in the dataframe
        row : VisumTable.Row
            a recordclass to compare the values
        """
        df_row = table.df.reset_index().iloc[rowno].tolist()
        assert df_row == list(row)
