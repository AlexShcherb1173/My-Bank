import unittest
from unittest.mock import MagicMock, mock_open, patch
from main import *


class TestMain(unittest.TestCase):

    @patch("main.os.chdir")
    @patch(
        "main.input",
        side_effect=[
            "json",  # input_choice
            "EXECUTED",  # input_state
            "да",
            "по убыванию",  # input_sort_date
            "да",  # input_sort_currency
            "да",
            "оплата",  # input_descr + слово
        ],
    )
    @patch("main.input_choice", return_value="json")
    @patch("main.input_state", return_value="EXECUTED")
    @patch("main.input_sort_date", return_value=[True, True])
    @patch("main.input_sort_currency", return_value=True)
    @patch("main.input_descr", return_value=True)
    @patch("main.read_json_file")
    @patch("main.transform_transactions")
    @patch("main.filter_by_state")
    @patch("main.sort_by_date")
    @patch("main.filter_and_sort_by_currency")
    @patch("main.process_bank_search")
    @patch("main.replace_nan_with_zero")
    @patch("main.format_transactions", return_value="Formatted Output")
    @patch("main.print")
    def test_full_run_json_flow(
        self,
        mock_print,
        mock_format,
        mock_replace,
        mock_process,
        mock_filter_currency,
        mock_sort_by_date,
        mock_filter_by_state,
        mock_transform,
        mock_read_json,
        mock_descr,
        mock_currency,
        mock_date,
        mock_state,
        mock_choice,
        mock_input,
        mock_chdir,
    ):
        # Подготовка фейковых данных на каждом этапе
        mock_read_json.return_value = [{"id": 1}]
        mock_transform.return_value = [{"id": 1}]
        mock_filter_by_state.return_value = [{"id": 1}]
        mock_sort_by_date.return_value = [{"id": 1}]
        mock_filter_currency.return_value = [{"id": 1}]
        mock_process.return_value = [{"id": 1}]
        mock_replace.return_value = [{"id": 1}]

        main()

        mock_print.assert_any_call("для обработки выбран json файл")
        mock_print.assert_any_call("Всего банковских операций в выборке 1\n")
        mock_print.assert_any_call("Formatted Output")