import unittest
from unittest.mock import patch, mock_open
import tempfile
import os
import json
from src_old.utils import read_json_file


class TestReadJsonFile(unittest.TestCase):

    def test_valid_json_list_of_dicts(self):
        data = [{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]
        with tempfile.NamedTemporaryFile('w+', delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, data)
        os.remove(f_path)

    def test_file_does_not_exist(self):
        result = read_json_file("nonexistent_file.json")
        self.assertEqual(result, [])

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_invalid_json_format(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            f.write("this is not json")
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_json_not_a_list(self):
        data = {"amount": 100}
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_json_list_not_dicts(self):
        data = [1, 2, 3]
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]))
    @patch("os.path.exists", return_value=True)
    def test_read_valid_json(self, mock_exists, mock_file):
        result = read_json_file("dummy_path.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)

    @patch("builtins.open", new_callable=mock_open, read_data="not json")
    @patch("os.path.exists", return_value=True)
    def test_read_invalid_json(self, mock_exists, mock_file):
        result = read_json_file("dummy_path.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=False)
    def test_file_not_exists(self, mock_exists):
        result = read_json_file("missing.json")
        self.assertEqual(result, [])
