import json
import os
import tempfile
import unittest

from tcx2rk.__main__ import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp(prefix='tcx2rk_tests_')
        self._our_dir = os.path.dirname(os.path.realpath(__file__))

    def test_convert_tcx_file(self):
        self.assert_conversion('test')

    def test_convert_tcx_file_single_lap(self):
        self.assert_conversion('test_single_lap')

    def assert_conversion(self, test_file_prefix):
        tcx_filepath = os.path.join(
            self._our_dir, 'data', '%s.tcx' % test_file_prefix)
        actual_output_file = os.path.join(
            self._tmp_dir, '%s.json' % test_file_prefix)

        main(tcx_filepath, actual_output_file)

        expected_output_file = os.path.join(
            self._our_dir, 'expected', '%s.json' % test_file_prefix)

        expected = self._load_json_file(expected_output_file)
        actual = self._load_json_file(actual_output_file)
        self.assertEqual(expected, actual)

    @staticmethod
    def _load_json_file(filepath):
        with open(filepath) as f:
            return json.load(f)
