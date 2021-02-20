from lxml import etree
import os, sys, copy

ENCODINGS = ['UTF-8', 'CP1252', 'ISO-8859-1']
DEFAULT_ENCODING = 'UTF-8'

DEFAULT_SRID = 3044
DEFAULT_FILE = os.path.join(os.path.split((sys.argv)[0])[0], "config.xml")

setting_struct = {
    'db_config': {
        'username': 'name',
        'password': 'pass',
        'db_name': 'db',
        'host': 'localhost',
        'port': '5432',
        'srid': DEFAULT_SRID,
    },
    'env': {
        'psql_path': 'dlls/psql.exe',
        'shp2pgsql_path': 'dlls/shp2pgsql.exe',
        'pgsql2shp_path': 'dlls/pgsql2shp.exe'
    },
    'recent': {
        'stations': '-1',
        'aggregations': '-1',
        'scenario': '-1',
        'download_tables_folder': '',
        'download_results_folder': '',
    }
}


'''
Borg pattern, all subclasses share same state (similar to singleton,
but without single identity)
'''
class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state


'''
holds informations about the environment and database settings
'''
class Config(Borg):

    def __init__(self):
        Borg.__init__(self)

    def read(self, filename=None):
        '''
        read the config from given xml file (default config.xml)
        '''

        if not filename:
            filename = DEFAULT_FILE

        # create file if it does not exist
        if not os.path.isfile(filename):
            self.settings = copy.deepcopy(setting_struct)
            self.write(filename)
        tree = etree.parse(filename)
        self.settings = copy.deepcopy(setting_struct)
        f_set = xml_to_dict(tree.getroot())
        for key, value in f_set.items():
            self.settings[key].update(value)

    def write(self, filename=None):
        '''
        write the config as xml to given file (default config.xml)
        '''

        if not filename:
            filename = DEFAULT_FILE

        xml_tree = etree.Element('CONFIG')
        dict_to_xml(xml_tree, self.settings)
        etree.ElementTree(xml_tree).write(str(filename), pretty_print=True)

def dict_to_xml(element, dictionary):
    '''
    append the entries of a dictionary as childs to the given xml tree element
    '''
    if isinstance(dictionary, list):
        for value in dictionary:
            elem = etree.Element('value')
            element.append(elem)
            if isinstance(dictionary, list) or isinstance(dictionary, dict):
                dict_to_xml(elem, value)
    elif not isinstance(dictionary, dict):
        element.text = str(dictionary)
    else:
        for key in dictionary:
            elem = etree.Element(key)
            element.append(elem)
            dict_to_xml(elem, dictionary[key])

def xml_to_dict(tree, represented_as_arrays=[]):
    '''
    convert a xml tree to a dictionary
    represented_as_arrays: list of Strings, all XML Tags, which should be handled
    as arrays
    '''
    if tree.tag in represented_as_arrays:
        value = []
        for child in tree.getchildren():
            value.append(xml_to_dict(child, represented_as_arrays))
    elif len(tree.getchildren()) > 0:
        value = {}
        for child in tree.getchildren():
            value[child.tag] = xml_to_dict(child, represented_as_arrays)
    else:
        value = tree.text
        if not value:
            value = ''
    return value
