from lxml import etree
import os, sys, copy

DEFAULT_SRID = 3044
DEFAULT_FILE = os.path.join(os.path.split((sys.argv)[0])[0], "config.xml")

setting_struct = {
    'db_config': {
        'username': 'name',
        'password': 'pass',
        'db_name': 'db',
        'host': 'localhost',
        'port': '5432',
        'srid': '3044'
        },
    'env': {
        'psql_path': '',
        'shp2pgsql_path': '',
        'pgsql2shp_path': ''
        }
}


'''
Borg pattern, all subclasses share same state (similar to singleton, but without single identity)
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

    '''
    read the config from given xml file (default config.xml)
    '''
    def read(self, filename=None):
        self.filename = filename if filename else DEFAULT_FILE

        # create file if it does not exist
        if not os.path.isfile(self.filename):
            self.settings = copy.deepcopy(setting_struct)
            self.write(self.filename)
        tree = etree.parse(self.filename)
        self.settings = copy.deepcopy(setting_struct) 
        f_set = xml_to_dict(tree.getroot())
        for key, value in f_set.iteritems():            
            self.settings[key].update(value)

    '''
    write the config as xml to given file (default config.xml)
    '''
    def write(self, filename=None):
        xml_tree = etree.Element('CONFIG')
        dict_to_xml(xml_tree, self.settings)
        if not filename:
            filename = self.filename
        etree.ElementTree(xml_tree).write(str(filename), pretty_print=True)

'''
append the entries of a dictionary as childs to the given xml tree element
'''
def dict_to_xml(element, dictionary):
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

'''
convert a xml tree to a dictionary
represented_as_arrays: list of Strings, all XML Tags, which should be handled as arrays
'''
def xml_to_dict(tree, represented_as_arrays=[]):
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
