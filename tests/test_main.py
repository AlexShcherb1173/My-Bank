import unittest
from unittest.mock import MagicMock, mock_open, patch
from main import *


class TestMainProgram(unittest.TestCase):

    @patch("main.print")
    @patch("builtins.input", side_effect=[
        "1",         # input_choice
        "EXECUTED",     # input_state
        "да", "по убыванию",  # input_sort_date
        "нет",               # input_sort_currency
        "да", "налог"         # input_descr + keyword
    ])
    @patch("main.read_json_file")
    @patch("main.transform_json")
    @patch("main.filter_by_state")
    @patch("main.sort_by_date")
    @patch("main.filter_and_sort_by_currency")
    @patch("main.process_bank_search")
    @patch("main.replace_nan_with_zero")
    @patch("main.format_transactions", return_value="Mock Result")
    def test_json_flow(self, mock_format, mock_clean, mock_search, mock_currency,
                       mock_sort, mock_filter, mock_transform, mock_read_json,
                       mock_input, mock_print):

        mock_read_json.return_value = [{"id": 1}]
        mock_transform.return_value = [{"id": 1}]
        mock_filter.return_value = [{"id": 1}]
        mock_sort.return_value = [{"id": 1}]
        mock_currency.return_value = [{"id": 1}]
        mock_search.return_value = [{"id": 1}]
        mock_clean.return_value = [{"id": 1}]

        main()

        mock_read_json.assert_called_once()
        mock_transform.assert_called_once()
        mock_filter.assert_called_once()
        mock_sort.assert_called_once()
        mock_currency.assert_not_called()  # потому что ввод: "нет"
        mock_search.assert_called_once()
        mock_clean.assert_called_once()
        mock_format.assert_called_once()

    @patch("main.print")
    @patch("builtins.input", side_effect=[
        "2", "EXECUTED", "нет", "да", "да", "покупка"
    ])
    @patch("main.read_transactions_from_csv")
    @patch("main.filter_by_state")
    @patch("main.sort_by_date")
    @patch("main.filter_and_sort_by_currency")
    @patch("main.process_bank_search")
    @patch("main.replace_nan_with_zero")
    @patch("main.format_transactions", return_value="CSV Mock Result")
    def test_csv_flow(self, mock_format, mock_clean, mock_search, mock_currency,
                      mock_sort, mock_filter, mock_read_csv,
                      mock_input, mock_print):

        mock_read_csv.return_value = [{"id": 2}]
        mock_filter.return_value = [{"id": 2}]
        mock_currency.return_value = [{"id": 2}]
        mock_search.return_value = [{"id": 2}]
        mock_clean.return_value = [{"id": 2}]

        main()

        mock_read_csv.assert_called_once()
        mock_filter.assert_called_once()
        mock_sort.assert_not_called()  # потому что сортировка по дате: "нет"
        mock_currency.assert_called_once()
        mock_search.assert_called_once()
        mock_clean.assert_called_once()
        mock_format.assert_called_once()

    @patch("main.print")
    @patch("builtins.input", side_effect=[
        "3", "CANCELED", "нет", "нет", "нет"
    ])
    @patch("main.read_transactions_from_excel")
    @patch("main.filter_by_state")
    @patch("main.sort_by_date")
    @patch("main.filter_and_sort_by_currency")
    @patch("main.process_bank_search")
    @patch("main.replace_nan_with_zero")
    @patch("main.format_transactions", return_value="XLSX Mock Result")
    def test_xlsx_flow(self, mock_format, mock_clean, mock_search, mock_currency,
                       mock_sort, mock_filter, mock_read_excel,
                       mock_input, mock_print):

        mock_read_excel.return_value = [{"id": 3}]
        mock_filter.return_value = [{"id": 3}]
        mock_clean.return_value = [{"id": 3}]

        main()

        mock_read_excel.assert_called_once()
        mock_filter.assert_called_once()
        mock_sort.assert_not_called()
        mock_currency.assert_not_called()
        mock_search.assert_not_called()
        mock_clean.assert_called_once()
        mock_format.assert_called_once()