import unittest
from unittest.mock import * #patch, mock_open
from src_old.utils_new import read_json_file


class TestUtilsReadJsonFile(unittest.TestCase):

    @patch("utils_new.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
    def test_read_valid_json(self, mock_file, mock_exists, mock_logger):
        result = read_json_file("valid.json")
        self.assertEqual(len(result), 2)
        mock_logger.debug.assert_called_once_with("Файл успешно прочитан: valid.json, найдено записей: 2")

    @patch("utils_new.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1}')
    def test_read_json_not_list(self, mock_file, mock_exists, mock_logger):
        result = read_json_file("not_list.json")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Некорректный формат данных в файле: not_list.json")

    @patch("utils_new.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_read_invalid_json(self, mock_file, mock_exists, mock_logger):
        result = read_json_file("broken.json")
        self.assertEqual(result, [])
        self.assertTrue(mock_logger.error.called)
        call_args = mock_logger.error.call_args[0][0]
        self.assertIn("Ошибка декодирования JSON", call_args)

    @patch("utils_new.logger")
    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists, mock_logger):
        result = read_json_file("missing.json")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Файл не найден: missing.json")

    @patch("utils_new.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_io_error(self, mock_file, mock_exists, mock_logger):
        result = read_json_file("file.json")
        self.assertEqual(result, [])
        self.assertTrue(mock_logger.error.called)
        self.assertIn("I/O ошибка при чтении файла", mock_logger.error.call_args[0][0])