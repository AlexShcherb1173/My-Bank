import unittest
import os
from unittest.mock import patch, mock_open
from src_old.freader import read_transactions_from_csv
from src_old.freader import read_transactions_from_excel

CSV_DATA = """id,state,date,amount,currency_name,currency_code,from,to,description
650703,EXECUTED,2023-09-05T11:30:32Z,16210,Sol,PEN,Счет 5880,Счет 3974,Перевод организации
"""
os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")

@patch(r"src\freader.logger")
@patch(r"src\freader.os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data=CSV_DATA)
def test_read_valid_csv(self, mock_file, mock_exists, mock_logger):
        result = read_transactions_from_csv("transactions.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["currency_code"], "PEN")
        mock_logger.debug.assert_called_once_with(
            "Файл CSV успешно прочитан: transactions.csv, записей: 1"
        )

@patch("freader.logger")
@patch("freader.os.path.exists", return_value=False)
def test_file_not_found(self, mock_exists, mock_logger):
        result = read_transactions_from_csv("missing.csv")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Файл CSV не найден: missing.csv")

@patch("freader.logger")
@patch("freader.os.path.exists", return_value=True)
@patch("builtins.open", side_effect=IOError("Permission denied"))
def test_open_error(self, mock_open_fn, mock_exists, mock_logger):
        result = read_transactions_from_csv("bad.csv")
        self.assertEqual(result, [])
        self.assertTrue(mock_logger.error.called)
        self.assertIn("Ошибка при чтении CSV", mock_logger.error.call_args[0][0])


class TestExcelReader(unittest.TestCase):
    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    @patch("freader.logger")
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

    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    @patch("freader.logger")
    @patch("os.path.exists", return_value=False)
    def test_file_not_exists(self, mock_exists, mock_logger):
        result = read_transactions_from_excel("missing.xlsx")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with("Файл Excel не найден: missing.xlsx")

    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    @patch("freader.logger")
    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=Exception("Ошибка Excel"))
    def test_read_excel_error(self, mock_read_excel, mock_exists, mock_logger):
        result = read_transactions_from_excel("corrupt.xlsx")
        self.assertEqual(result, [])
        self.assertIn("Ошибка при чтении Excel", mock_logger.error.call_ar)