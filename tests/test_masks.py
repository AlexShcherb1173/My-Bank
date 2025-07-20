import unittest
from unittest.mock import patch
from src.masks import *

class TestMasks(unittest.TestCase):
    """test_mask_card_success ---     Маскирует валидную карту. Проверяет logger.debug
       test_mask_card_invalid --- Ошибка при маскировании(буквы). Проверяет logger.error
       test_mask_account_success --- Маскирует валидный счёт. Проверяет logger.debug
       test_mask_account_invalid --- Ошибка при маскировании(короткий ввод). Проверяет logger.error
    """

    @patch("masks.logger")
    def test_mask_card_success(self, mock_logger):
        card = "1234567812345678"
        expected = "1234 56** **** 5678"
        result = get_mask_card_number(card)
        self.assertEqual(result, expected)
        mock_logger.debug.assert_called_once_with(f"Успешное маскирование номера карты: {expected}")

    @patch("masks.logger")
    def test_mask_card_invalid(self, mock_logger):
        card = "abc"
        result = get_mask_card_number(card)
        self.assertEqual(result, "**** **** **** ****")
        self.assertTrue(mock_logger.error.called)
        mock_logger.error.assert_called_with("Ошибка при маскировании номера карты: Неверный формат номера карты")

    @patch("masks.logger")
    def test_mask_account_success(self, mock_logger):
        acc = "40817810099910004312"
        expected = "**4312"
        result = get_mask_acount(acc)
        self.assertEqual(result, expected)
        mock_logger.debug.assert_called_once_with(f"Успешное маскирование номера счёта: {expected}")

    @patch("masks.logger")
    def test_mask_account_invalid(self, mock_logger):
        acc = "12"
        result = get_mask_acount(acc)
        self.assertEqual(result, "**0000")
        self.assertTrue(mock_logger.error.called)
        mock_logger.error.assert_called_with("Ошибка при маскировании номера счёта: Неверный формат номера счёта")