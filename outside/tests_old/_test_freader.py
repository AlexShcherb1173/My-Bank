import unittest
import os
import sys
from unittest.mock import mock_open, patch, MagicMock
os.chdir(r"/")
from src_old.freader import *


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(r"/")
class TestReadTransactionsFromCSV(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="dummy")
    @patch("freader.transform_transaction")
    @patch("csv.DictReader")
    def test_read_transactions_from_csv(self, mock_dict_reader, mock_transform, mock_file):
        # Подготавливаем фейковые строки, которые возвращает csv.DictReader
        fake_rows = [
            {'id;state;amount;currency_name;from;to': '650703;EXECUTED;16210;Sol;Счет 58803664561298323391;Счет 39745660563456619397'},
            {'id;state;amount;currency_name;from;to': '111111;EXECUTED;33333;Sol;Счет 58803664561298323391;Счет 39745660563456619397'}
        ]
        mock_dict_reader.return_value = fake_rows

        # Подготавливаем то, что должна вернуть transform_transaction
        mock_transform.side_effect = [
            {'id': 650703.0, 'state': 'EXECUTED', 'amount': 16210.0, 'currency_name': 'Sol', 'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397'},
            {'id': 111111.0, 'state': 'EXECUTED', 'amount': 33333.0, 'currency_name': 'Sol', 'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397'}
        ]

        result = read_transactions_from_csv("fake_path.csv")

        self.assertEqual(result, [
            {'id': 650703.0, 'state': 'EXECUTED', 'amount': 16210.0, 'currency_name': 'Sol',
             'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397'},
            {'id': 111111.0, 'state': 'EXECUTED', 'amount': 33333.0, 'currency_name': 'Sol',
             'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397'}
        ])
        mock_file.assert_called_once_with("fake_path.csv", mode='r', encoding='utf-8')
        self.assertEqual(mock_transform.call_count, 0)

os.chdir(r"/")
class TestReadTransactionsFromExcel(unittest.TestCase):
    @patch("freader.pd.read_excel")
    def test_read_transactions_from_excel(self, mock_read_excel):
        # Подготовка фейкового DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200}
        ]
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("fake_path.xlsx")

        # Проверка
        self.assertEqual(result, [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200}
        ])
        mock_read_excel.assert_called_once_with("fake_path.xlsx")
        mock_df.to_dict.assert_called_once_with(orient="records")