import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verschneidungstool.config import Borg, Config, setting_struct


class ConfigDefaultsTests(unittest.TestCase):
    def setUp(self):
        shared_state = patch.dict(Borg._shared_state, {}, clear=True)
        shared_state.start()
        self.addCleanup(shared_state.stop)

    def test_constructor_provides_defaults_without_file_access(self):
        with patch.object(Config, 'read') as read, patch.object(Config, 'write') as write:
            config = Config()
        self.assertEqual(config.settings, setting_struct)
        self.assertIsNot(config.settings, setting_struct)
        config.settings['db_config']['host'] = 'custom'
        self.assertNotEqual(setting_struct['db_config']['host'], 'custom')
        read.assert_not_called()
        write.assert_not_called()

    def test_existing_shared_settings_are_preserved_and_completed(self):
        first = Config()
        first.settings = {'db_config': {'host': 'project-db'}, 'env': {}}
        second = Config()
        self.assertIs(first.settings, second.settings)
        self.assertEqual(second.settings['db_config']['host'], 'project-db')
        self.assertEqual(second.settings['recent'], setting_struct['recent'])
        self.assertIn('srid', second.settings['db_config'])

    def test_standalone_xml_can_still_be_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.xml'
            config = Config()
            config.settings['db_config']['host'] = 'saved-db'
            config.write(path)
            saved = copy.deepcopy(config.settings)
            Borg._shared_state.clear()
            restored = Config()
            restored.read(path)
            self.assertEqual(restored.settings['db_config']['host'], 'saved-db')
            self.assertEqual(restored.settings['env'], saved['env'])


if __name__ == '__main__':
    unittest.main()
