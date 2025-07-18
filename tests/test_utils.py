import unittest
import tempfile
import os
import json
from src.utils import read_json_file

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