"""Run with: python -m unittest discover -s tests (with src on PYTHONPATH)."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import unittest
import re
from types import SimpleNamespace as Row
from unittest.mock import MagicMock, patch

from PyQt5.QtWidgets import QApplication, QDialog
from verschneidungstool.dialogs import UploadAreaDialog, UploadShapeDialog
from verschneidungstool.model import DBConnection
from psycopg2.extras import NamedTupleCursor


class AreaDialogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.db = MagicMock()
        self.db.get_projections_available.return_value = [Row(srid=3044, name='ETRS')]
        self.db.get_polygon_layers.return_value = [
            Row(table_name='zones', geometry_column='shape', relkind='v'),
            Row(table_name='cached', geometry_column='geom', relkind='m')]
        self.db.get_column_names.return_value = [Row(column_name=c) for c in ('id', 'name', 'shape')]
        self.db.set_zone.return_value = (True, '')
        self.finished, self.success = MagicMock(), MagicMock()
        self.dialog = UploadAreaDialog(self.db, ['public', 'other'],
                                       on_finish=self.finished, on_success=self.success)
        self.dialog.warn = MagicMock()
        self.addCleanup(self.dialog.deleteLater)

    def test_existing_view_registration_and_callbacks(self):
        d = self.dialog
        d.existing_radio.setChecked(True)
        self.assertEqual(d.layer_combo.itemText(0), 'zones (View)')
        self.assertEqual(d.layer_combo.itemText(1), 'cached (Materialisierte View)')
        self.assertTrue(d.shapefile_edit.isHidden())
        d.area_name_edit.setText('Meine Gebiete 2026')
        d.upload()
        self.db.register_existing_area.assert_not_called()
        self.assertEqual(d.pkey_combo.count(), 2)
        d.names_combo.setCurrentText('name')
        d.OK_button.click()
        self.db.register_existing_area.assert_called_once_with(
            'public', 'zones', 'Meine Gebiete 2026', 'id', 'name')
        self.db.set_zone.assert_not_called()
        self.assertEqual(d.result(), QDialog.Accepted)
        self.finished.assert_called_once_with()
        self.success.assert_called_once_with()

    def test_empty_schema_and_switch_back(self):
        d = self.dialog
        d.existing_radio.setChecked(True)
        self.db.get_polygon_layers.return_value = []
        d.schema_combo.setCurrentIndex(1)
        self.assertEqual(d.layer_combo.count(), 0)
        d.upload()
        d.warn.assert_called_once()
        self.assertFalse(d.OK_button.isEnabled())
        d.shape_radio.setChecked(True)
        self.assertFalse(d.shapefile_edit.isHidden())
        self.assertTrue(d.layer_combo.isHidden())

    def test_invalid_id_keeps_dialog_open(self):
        d = self.dialog
        d.existing_radio.setChecked(True)
        d.upload()
        self.db.register_existing_area.side_effect = ValueError('Doppelte ID')
        d.OK_button.click()
        d.warn.assert_called_once()
        self.finished.assert_not_called()
        self.assertNotEqual(d.result(), QDialog.Accepted)

    def test_shape_retains_table_name_and_sets_display_name(self):
        d = self.dialog
        d.schema, d.name = 'public', 'legacy_table'
        self.db.get_areas_available.return_value = [Row(schema='public', table_name='legacy_table')]
        with patch.object(UploadShapeDialog, 'upload', return_value=True):
            d.upload()
        d.area_name_edit.setText('Frei gewählter Name')
        d.OK_button.click()
        self.db.set_zone.assert_called_once()
        self.db.set_area_display_name.assert_called_once_with(
            'public', 'legacy_table', 'Frei gewählter Name')
        self.finished.assert_called_once_with()

    def test_legacy_auto_arguments(self):
        self.db.get_areas_available.return_value = [Row(schema='public', table_name='legacy_table')]
        args = dict(shape_path='zones.shp', schema='public', table_name='legacy_table',
                    srid=3044, c_id='id', c_name='name')
        with patch.object(UploadShapeDialog, 'upload', return_value=True):
            dialog = UploadAreaDialog(self.db, ['public'], auto_args=args)
        self.addCleanup(dialog.deleteLater)
        self.assertEqual(dialog.result(), QDialog.Accepted)
        self.db.set_area_display_name.assert_called_once_with('public', 'legacy_table', 'legacy_table')


class IntersectionTests(unittest.TestCase):
    def test_view_with_custom_geometry_without_coordinate_columns(self):
        db = DBConnection(None)
        db.get_column_names = MagicMock(return_value=[Row(column_name=c) for c in ('id', 'shape')])
        db.get_polygon_layers = MagicMock(return_value=[Row(table_name='zones', geometry_column='shape')])
        db.fetch = MagicMock(side_effect=[[Row(pkey='id', zone_id='id', zone_name='id')], [], [(1,)]])
        db.execute = MagicMock()
        thread = db.new_intersection('public', 'zones', srid=3044)
        errors = []
        thread.error.connect(errors.append)
        thread.run()
        self.assertEqual(errors, [])
        polygon_view = db.execute.call_args_list[0].args[0]
        point_view = db.execute.call_args_list[1].args[0]
        self.assertIn('st_transform(t."shape", 3044)', polygon_view)
        self.assertNotIn('xcoord', polygon_view)
        self.assertIn('st_transform(t."shape", 3044)', point_view)

    def test_legacy_coordinates_and_point_column_are_preserved(self):
        db = DBConnection(None)
        db.get_column_names = MagicMock(return_value=[Row(column_name=c) for c in ('id', 'geom', 'xcoord', 'ycoord', 'pnt')])
        db.get_polygon_layers = MagicMock(return_value=[Row(table_name='zones', geometry_column='geom')])
        db.fetch = MagicMock(side_effect=[[Row(pkey='id', zone_id='id', zone_name='id')], [], [(1,)]])
        db.execute = MagicMock()
        db.new_intersection('public', 'zones').run()
        self.assertIn('st_makepoint(t.xcoord, t.ycoord)', db.execute.call_args_list[0].args[0])
        self.assertIn('t."pnt"', db.execute.call_args_list[1].args[0])


class RegistrationTests(unittest.TestCase):
    def register(self, counts, duplicate=False):
        db = DBConnection(None)
        db.get_polygon_layers = MagicMock(return_value=[Row(table_name='zones')])
        db.get_column_names = MagicMock(return_value=[Row(column_name='id')])
        self.conn = MagicMock()
        self.cursor = self.conn.cursor.return_value
        self.cursor.fetchone.side_effect = [counts, (1,) if duplicate else None]
        with patch('verschneidungstool.model.Connection') as connection:
            connection.return_value.__enter__.return_value = self.conn
            db.register_existing_area('public', 'zones', "Region O'Brien", 'id')

    def test_register_only_writes_metadata(self):
        self.register((3, 3, 3, 3, True))
        insert, params = self.cursor.execute.call_args.args
        self.assertIn('INSERT INTO', str(insert))
        self.assertRegex(str(insert), r'VALUES \(%s, %s, %s, TRUE,')
        self.assertEqual(params, ("Region O'Brien", 'public', 'zones', 'id', 'id', 'id'))
        self.conn.commit.assert_called_once()

    def test_id_validation_result_has_unique_named_tuple_fields(self):
        self.register((3, 3, 3, 3, True))
        query = self.cursor.execute.call_args_list[0].args[0]
        fields = tuple(re.findall(r'\bAS\s+(\w+)', str(query)))
        self.assertEqual(len(fields), 5)
        record_type = NamedTupleCursor._do_make_nt(fields)
        result = record_type(3, 3, 3, 3, True)
        self.assertEqual(tuple(result), (3, 3, 3, 3, True))

    def test_reject_null_duplicate_empty_and_noninteger_ids(self):
        for counts in [(0, 0, 0, 0, None), (3, 2, 2, 2, True),
                       (3, 3, 2, 2, True), (3, 3, 3, 2, True), (3, 3, 3, 3, False)]:
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                self.register(counts)
            self.conn.commit.assert_not_called()

    def test_reject_duplicate_registration(self):
        with self.assertRaises(ValueError):
            self.register((3, 3, 3, 3, True), duplicate=True)
        self.conn.commit.assert_not_called()


class RemovalTests(unittest.TestCase):
    def test_standalone_removal_also_drops_source_table(self):
        db = DBConnection(None)
        db.get_last_calculated = MagicMock(return_value=[])
        db.execute = MagicMock()
        success, message = db.drop_area(7, 'zones', 'public')
        self.assertTrue(success)
        self.assertEqual(db.execute.call_count, 2)
        query = db.execute.call_args_list[0].args[0].upper()
        self.assertIn('DELETE FROM', query)
        self.assertIn('AREAS_AVAILABLE', query)
        self.assertEqual(db.execute.call_args_list[1].args[0], 'DROP TABLE IF EXISTS "public"."zones"')

    def test_latest_calculation_guard_returns_message_without_deleting(self):
        db = DBConnection(None)
        db.get_last_calculated = MagicMock(return_value=[Row(schema='public', table_name='zones')])
        db.execute = MagicMock()
        success, message = db.drop_area(7, 'zones', 'public')
        self.assertFalse(success)
        self.assertIn('letzte Verschneidung', message)
        db.execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
