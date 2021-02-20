# -*- coding: utf-8 -*-

import os
import pandas as pd


class VisumAttributes:
    """
    Store the contents of the attribute.xlsx-file in an hdf5-file
    purpose is to automatically create the VisumTable classes
    """
    @classmethod
    def from_excel(cls, h5file: str, visum_version: int = 20, language='Deu'):

        self = super().__new__(cls)
        visum_attribute_file = 'attribute.xlsx'
        visum_folder = rf'C:\Program Files\PTV Vision\PTV Visum {visum_version}\Doc\{language}'
        fn = os.path.join(visum_folder, visum_attribute_file)
        self.tables = pd.read_excel(fn, sheet_name='Tables', usecols=5)\
            .set_index('Name')
        self.attributes = pd.read_excel(fn, sheet_name='Attributes',
                                        usecols=19)\
            .set_index(['Object', 'AttributeID'])
        self.relations = pd.read_excel(fn, sheet_name='Relation', usecols=7)\
            .set_index(['TabFrom', 'TabTo', 'RoleName'])
        self.subattributes = pd.read_excel(fn, sheet_name='SubAttributes',
                                           usecols=6)\
            .set_index(['SubAttrName'])

        #self.enumliterals = pd.read_excel(fn, sheet_name='EnumLiterals',
                                          #usecols=9).set_index('Code')
        self.tables.to_hdf(h5file, 'tables', format='t', complevel=2)
        self.attributes.to_hdf(h5file, 'attributes', format='t',
                               complevel=2, mode='a')
        self.relations.to_hdf(h5file, 'relations', format='t',
                              complevel=2, mode='a')
        self.subattributes.to_hdf(h5file, 'subattributes', format='t',
                                  complevel=2, mode='a')
        #self.enumliterals.to_hdf(h5file, 'enumliterals', format='t',
        # complevel=2, mode='a')
        self.set_index()

    @classmethod
    def from_hdf(cls, h5file):
        self = super().__new__(cls)
        self.tables = pd.read_hdf(h5file, 'tables')
        self.attributes = pd.read_hdf(h5file, 'attributes')
        self.relations = pd.read_hdf(h5file, 'relations')
        self.subattributes = pd.read_hdf(h5file, 'subattributes')
        self.set_index()
        return self

    def set_index(self):
        """set the shortGerman-name as index"""
        attrs = self.attributes.reset_index()
        attrs['col'] = attrs['AttributeShort(DEU)'].str.upper()
        is_empty = attrs['col'].isna()
        attrs.loc[is_empty, 'col'] = attrs.loc[is_empty,
                                               'AttributeID'].str.upper()
        attrs = attrs.set_index(['Object', 'col'])
        self.attributes = attrs
