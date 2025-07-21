import unittest
from unittest.mock import patch, mock_open
from src.reader import read_transactions_from_csv
from src.reader import read_transactions_from_excel

CSV_DATA = """id\tstate\tdate\tamount\tcurrency_name\tcurrency_code\tfrom\tto\tdescription
650703\tEXECUTED\t2023-09-05T11:30:32Z\t16210\tSol\tPEN\tСчет 5880\tСчет 3974\tПеревод организации
"""

class TestCSVReader(unittest.TestCase):

    @patch(r"logs\.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
    def test_read_valid_csv(self, mock_file, mock_exists, mock_logger):
        result = read_transactions_from_csv("test.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['currency_code'], 'PEN')
        mock_logger.debug.assert_called_once()

    @patch(r"logs\er.logger")
    @patch("os.path.exists", return_value=False)
    def test_file_not_exists(self, mock_exists, mock_logger):
        result = read_transactions_from_csv("missing.csv")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Файл CSV не найден: missing.csv")

    @patch(r"logs\r.logger")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_io_error(self, mock_file, mock_exists, mock_logger):
        result = read_transactions_from_csv("bad.csv")
        self.assertEqual(result, [])
        self.assertIn("Ошибка при чтении CSV", mock_logger.error.call_args[0][0])


class TestExcelReader(unittest.TestCase):

    @patch(r"logs\reader.logger")
    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel")
    def test_read_valid_excel(self, mock_read_excel, mock_exists, mock_logger):
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"id": 1, "currency_code": "EUR"}]
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("test.xlsx")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["currency_code"], "EUR")
        mock_logger.debug.assert_called_once()

    @patch(r"logs\reader.logger")
    @patch("os.path.exists", return_value=False)
    def test_file_not_exists(self, mock_exists, mock_logger):
        result = read_transactions_from_excel("missing.xlsx")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Файл Excel не найден: missing.xlsx")

    @patch(r"logs\.logger")
    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=Exception("Ошибка Excel"))
    def test_read_excel_error(self, mock_read_excel, mock_exists, mock_logger):
        result = read_transactions_from_excel("corrupt.xlsx")
        self.assertEqual(result, [])
        self.assertIn("Ошибка при чтении Excel", mock_logger.error.call_ar