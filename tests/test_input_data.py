import unittest
from unittest.mock import MagicMock, mock_open, patch
from input_data import *


class TestUserInputs(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    def test_input_choice_json(self, mock_input):
        self.assertEqual(input_choice(), "JSON")

    @patch("builtins.input", side_effect=["2"])
    def test_input_choice_csv(self, mock_input):
        self.assertEqual(input_choice(), "CSV")

    @patch("builtins.input", side_effect=["3"])
    def test_input_choice_xlsx(self, mock_input):
        self.assertEqual(input_choice(), "XLSX")

    @patch("builtins.input", side_effect=["wrong", "5", "2"])
    def test_input_choice_invalid_then_valid(self, mock_input):
        self.assertEqual(input_choice(), "CSV")

    @patch("builtins.input", side_effect=["executed"])
    def test_input_state_executed(self, mock_input):
        self.assertEqual(input_state(), "EXECUTED")

    @patch("builtins.input", side_effect=["pending"])
    def test_input_state_pending(self, mock_input):
        self.assertEqual(input_state(), "PENDING")

    @patch("builtins.input", side_effect=["cancel", "canceled"])
    def test_input_state_retry(self, mock_input):
        self.assertEqual(input_state(), "CANCELED")

    @patch("builtins.input", side_effect=["да", "по убыванию"])
    def test_input_sort_date_descending(self, mock_input):
        self.assertEqual(input_sort_date(), [True, True])

    @patch("builtins.input", side_effect=["нет"])
    def test_input_sort_date_none(self, mock_input):
        self.assertEqual(input_sort_date(), [False])

    @patch("builtins.input", side_effect=["да"])
    def test_input_sort_currency_true(self, mock_input):
        self.assertTrue(input_sort_currency())

    @patch("builtins.input", side_effect=["нет"])
    def test_input_sort_currency_false(self, mock_input):
        self.assertFalse(input_sort_currency())

    @patch("builtins.input", side_effect=["да", "налог"])
    def test_input_descr_yes(self, mock_input):
        self.assertEqual(input_descr(), ["да", "налог"])

    @patch("builtins.input", side_effect=["нет"])
    def test_input_descr_no(self, mock_input):
        self.assertEqual(input_descr(), ["нет"])
