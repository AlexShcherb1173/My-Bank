import unittest
from unittest.mock import MagicMock, mock_open, patch
from input_data import *


class TestInputChoice(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    def test_valid_json_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "json")

    @patch("builtins.input", side_effect=["2"])
    def test_valid_csv_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "csv")

    @patch("builtins.input", side_effect=["3"])
    def test_valid_xlsx_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "xlsx")

    @patch("builtins.input", side_effect=["0", "4", "abc", "", "2"])
    def test_invalid_then_valid_input(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "csv")

    @patch("builtins.input", side_effect=["abc", "!", "3"])
    def test_multiple_invalid_then_valid(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "xlsx")

class TestInputSortDate(unittest.TestCase):
    @patch("builtins.input", side_effect=["Да", "по убыванию"])
    def test_sort_yes_descending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, True])

    @patch("builtins.input", side_effect=["Да", "по возрастанию"])
    def test_sort_yes_ascending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])

    @patch("builtins.input", side_effect=["Нет"])
    def test_sort_no(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [False])

    @patch("builtins.input", side_effect=["abc", "да", "убыванию"])
    def test_invalid_then_valid_descending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, True])

    @patch("builtins.input", side_effect=["123", "Нет"])
    def test_invalid_then_valid_no(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [False])

    @patch("builtins.input", side_effect=["ДА", "ВОЗРАСТАНИЮ"])
    def test_upper_case_input(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])

    @patch("builtins.input", side_effect=["да", "сначала старые", "по возрастанию"])
    def test_invalid_sort_direction_then_valid(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])


class TestInputSortCurrency(unittest.TestCase):

    @patch("builtins.input", side_effect=["Да"])
    def test_rub_currency_yes(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["Нет"])
    def test_rub_currency_no(self, mock_input):
        result = input_sort_currency()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["abc", "ДА"])
    def test_invalid_then_valid_uppercase_yes(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["123", "нет"])
    def test_invalid_numeric_then_valid_no(self, mock_input):
        result = input_sort_currency()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["", "что-то", "да"])
    def test_multiple_invalid_then_valid(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)


class TestInputDescr(unittest.TestCase):

    @patch("builtins.input", side_effect=["Да"])
    def test_filter_yes(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["Нет"])
    def test_filter_no(self, mock_input):
        result = input_descr()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["ДА"])
    def test_uppercase_yes(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["нет"])
    def test_lowercase_no(self, mock_input):
        result = input_descr()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["123", "abc", "Да"])
    def test_invalid_then_valid(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["", "нет"])
    def test_empty_then_valid(self, mock_input):
        result = input_descr()
        self.assertFalse(result)
