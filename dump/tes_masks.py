# tes_masks.py
import unittest
from unittest.mock import patch
import masks


class TestMasks(unittest.TestCase):

    def test_get_mask_card_number_valid(self):
        result = masks.get_mask_card_number("1234567890123456")
        expected = "1234 56** **** 3456"
        self.assertEqual(result, expected)

    def test_get_mask_card_number_invalid_short(self):
        with self.assertRaises(ValueError):
            masks.get_mask_card_number("123456")

    def test_get_mask_card_number_invalid_non_digit(self):
        with self.assertRaises(ValueError):
            masks.get_mask_card_number("abcd567890123456")

    def test_get_mask_acount_valid(self):
        result = masks.get_mask_acount("1234567890")
        expected = "**7890"
        self.assertEqual(result, expected)

    def test_get_mask_acount_invalid_short(self):
        with self.assertRaises(ValueError):
            masks.get_mask_acount("123")

    @patch("masks.logger")
    def test_logging_card_number_success(self, mock_logger):
        masks.get_mask_card_number("1234567890123456")
        mock_logger.debug.assert_called_once()
        mock_logger.error.assert_not_called()

    @patch("masks.logger")
    def test_logging_card_number_error(self, mock_logger):
        with self.assertRaises(ValueError):
            masks.get_mask_card_number("123")
        mock_logger.error.assert_called_once()

    @patch("masks.logger")
    def test_logging_acount_success(self, mock_logger):
        masks.get_mask_acount("9876543210")
        mock_logger.debug.assert_called_once()
        mock_logger.error.assert_not_called()

    @patch("masks.logger")
    def test_logging_acount_error(self, mock_logger):
        with self.assertRaises(ValueError):
            masks.get_mask_acount("12")
        mock_logger.error.assert_called_once()

