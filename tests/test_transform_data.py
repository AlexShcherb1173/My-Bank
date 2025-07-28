import unittest
from unittest.mock import MagicMock, mock_open, patch
import math
from reformat_rec import *
from transform_data import *


class TestFormatTransactions(unittest.TestCase):

    @patch("reformat_rec.get_date", return_value="01.01.2024")
    @patch("reformat_rec.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
    def test_single_transaction_with_sender_and_receiver(self, mock_mask, mock_date):
        transactions = [
            {
                "date": "2024-01-01T12:00:00Z",
                "description": "Перевод клиенту",
                "from": "Account1234567890",
                "to": "Account0987654321",
                "amount": 1000,
                "currency_name": "RUB",
            }
        ]
        expected_output = "01.01.2024 Перевод клиенту\n" "***7890 -> ***4321\n" "Сумма: 1000 RUB.\n"
        result = format_transactions(transactions)
        self.assertEqual(result.strip(), expected_output.strip())

    @patch("reformat_rec.get_date", return_value="15.07.2023")
    @patch("reformat_rec.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
    def test_transaction_without_sender(self, mock_mask, mock_date):
        transactions = [
            {
                "date": "2023-07-15T08:00:00Z",
                "description": "Открытие вклада",
                "to": "DepositAccount9876",
                "amount": 50000,
                "currency_name": "USD",
            }
        ]
        expected_output = "15.07.2023 Открытие вклада\n" "***9876\n" "Сумма: 50000 USD.\n"
        result = format_transactions(transactions)
        self.assertEqual(result.strip(), expected_output.strip())

    @patch("reformat_rec.get_date", return_value="")
    @patch("reformat_rec.mask_account_card", return_value="")
    def test_empty_transaction(self, mock_mask, mock_date):
        transactions = [{}]
        expected_output = "Сумма: 0 ."
        result = format_transactions(transactions)
        self.assertEqual(result.strip(), expected_output.strip())

    @patch("reformat_rec.get_date", return_value="05.05.2025")
    @patch("reformat_rec.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
    def test_multiple_transactions(self, mock_mask, mock_date):
        transactions = [
            {
                "date": "2025-05-05",
                "description": "Перевод",
                "from": "Card000011112222",
                "to": "Card999988887777",
                "amount": 1200,
                "currency_name": "EUR",
            },
            {
                "date": "2025-05-05",
                "description": "Пополнение",
                "to": "Card666655554444",
                "amount": 500,
                "currency_name": "RUB",
            },
        ]
        expected_output = (
            "05.05.2025 Перевод\n***2222 -> ***7777\nСумма: 1200 EUR.\n\n"
            "05.05.2025 Пополнение\n***4444\nСумма: 500 RUB.\n"
        )
        result = format_transactions(transactions)
        self.assertEqual(result.strip(), expected_output.strip())

class TestReplaceNanWithZero(unittest.TestCase):

    def test_no_nan_values(self):
        transactions = [{"id": 1, "amount": 100.0, "currency": "RUB"}, {"id": 2, "amount": 200.0, "currency": "USD"}]
        result = replace_nan_with_zero(transactions)
        self.assertEqual(result, transactions)

    def test_replace_nan_with_zero(self):
        transactions = [
            {"id": 1, "amount": math.nan, "currency": "RUB"},
            {"id": 2, "amount": 150.0, "currency": "USD"},
        ]
        expected = [
            {"id": 1, "amount": "0", "currency": "RUB"},
            {"id": 2, "amount": 150.0, "currency": "USD"},
        ]
        result = replace_nan_with_zero(transactions)
        self.assertEqual(result, expected)

    def test_multiple_nan_fields(self):
        transactions = [{"id": math.nan, "amount": math.nan, "currency": "EUR"}]
        expected = [{"id": "0", "amount": "0", "currency": "EUR"}]
        result = replace_nan_with_zero(transactions)
        self.assertEqual(result, expected)

    def test_non_float_nan_like_strings(self):
        transactions = [
            {"id": 1, "amount": "NaN", "currency": "USD"},  # строка "NaN" не должна заменяться
            {"id": 2, "amount": float("nan"), "currency": "USD"},
        ]
        result = replace_nan_with_zero(transactions)
        self.assertEqual(result[0]["amount"], "NaN")
        self.assertEqual(result[1]["amount"], "0")

    def test_empty_transaction_list(self):
        result = replace_nan_with_zero([])
        self.assertEqual(result, [])

class TestTransformCsv(unittest.TestCase):

    def test_valid_transaction(self):
        input_data = [
            {
                "id": "123",
                "state": "EXECUTED",
                "date": "2023.01.01",
                "operationAmount": {"amount": "1000.50", "currency": {"name": "Russian Ruble", "tests": "RUB"}},
                "description": "Payment",
                "from": "Account A",
                "to": "Account B",
            }
        ]
        result = transform_csv(input_data)
        expected = [
            {
                "id": 123.0,
                "state": "EXECUTED",
                "date": "2023Z",
                "amount": 1000.50,
                "currency_name": "Russian Ruble",
                "currency_code": "RUB",
                "from": "Account A",
                "to": "Account B",
                "description": "Payment",
            }
        ]
        self.assertEqual(result, expected)

    def test_missing_required_keys(self):
        input_data = [
            {
                "id": "123",
                "state": "EXECUTED",
                # missing 'date', 'to', etc.
                "operationAmount": {"amount": "1000.50", "currency": {"name": "RUB", "tests": "RUB"}},
                "description": "Payment",
            }
        ]
        result = transform_csv(input_data)
        self.assertEqual(result, [])

    def test_invalid_structure(self):
        input_data = ["not a dict", 123, None]
        result = transform_transactions(input_data)
        self.assertEqual(result, [])

    def test_malformed_operation_amount(self):
        input_data = [
            {
                "id": "123",
                "state": "EXECUTED",
                "date": "2023.01.01",
                "operationAmount": "not a dict",
                "description": "Payment",
                "to": "Account B",
            }
        ]
        result = transform_csv(input_data)
        self.assertEqual(result, [])

    def test_missing_from_field(self):
        input_data = [
            {
                "id": "456",
                "state": "EXECUTED",
                "date": "2023.05.01",
                "operationAmount": {"amount": "200", "currency": {"name": "Dollar", "tests": "USD"}},
                "description": "Transfer",
                "to": "Account C",
            }
        ]
        result = transform_csv(input_data)
        self.assertEqual(result[0]["from"], "")

    def test_invalid_id_and_amount_types(self):
        input_data = [
            {
                "id": "not-a-number",
                "state": "EXECUTED",
                "date": "2023.01.01",
                "operationAmount": {"amount": "also-bad", "currency": {"name": "USD", "tests": "USD"}},
                "description": "Broken",
                "to": "Account D",
            }
        ]
        result = transform_csv(input_data)
        self.assertEqual(result, [])




class TestTransformJson(unittest.TestCase):

    def test_valid_transaction(self):
        input_data = [{
            "id": "123",
            "state": "EXECUTED",
            "date": "2023.01.01T00:00:00",
            "operationAmount": {
                "amount": "1500.50",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            },
            "description": "Оплата",
            "from": "Счет 123",
            "to": "Счет 456"
        }]
        result = transform_json(input_data)
        expected = [{
            "id": 123.0,
            "state": "EXECUTED",
            "date": "2023Z",
            "amount": 1500.5,
            "currency_name": "RUB",
            "currency_code": "RUB",
            "from": "Счет 123",
            "to": "Счет 456",
            "description": "Оплата"
        }]
        self.assertEqual(result, expected)

    def test_missing_required_keys(self):
        input_data = [{
            "id": "124",
            "state": "EXECUTED",
            # нет ключей date, to и operationAmount
            "description": "Неполная запись"
        }]
        result = transform_json(input_data)
        self.assertEqual(result, [])

    def test_non_dict_input(self):
        input_data = [
            "not a dict",
            123,
            None,
            ["nested", "list"]
        ]
        result = transform_json(input_data)
        self.assertEqual(result, [])

    def test_missing_from_key(self):
        input_data = [{
            "id": "125",
            "state": "EXECUTED",
            "date": "2022.01.01T00:00:00",
            "operationAmount": {
                "amount": "2000.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод",
            # нет ключа "from"
            "to": "Счет 789"
        }]
        result = transform_json(input_data)
        self.assertEqual(result[0]["from"], "")

    def test_malformed_operation_amount(self):
        input_data = [{
            "id": "126",
            "state": "EXECUTED",
            "date": "2021.01.01T00:00:00",
            "operationAmount": "invalid_structure",  # не словарь
            "description": "Ошибка в структуре",
            "to": "Счет 101"
        }]
        result = transform_json(input_data)
        self.assertEqual(result, [])

    def test_invalid_amount_or_id_format(self):
        input_data = [{
            "id": "NaN",
            "state": "EXECUTED",
            "date": "2023.02.02T00:00:00",
            "operationAmount": {
                "amount": "bad",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            },
            "description": "Ошибка преобразования",
            "to": "Счет 303"
        }]
        result = transform_json(input_data)
        self.assertEqual(result, [])

    def test_multiple_mixed_records(self):
        input_data = [
            "строка",
            {"id": "1", "state": "EXECUTED"},  # неполная
            {
                "id": "10",
                "state": "EXECUTED",
                "date": "2023.05.05T00:00:00",
                "operationAmount": {
                    "amount": "300.00",
                    "currency": {"name": "GBP", "code": "GBP"}
                },
                "description": "Валидная",
                "to": "Счет 100"
            }
        ]
        result = transform_json(input_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["currency_code"], "GBP")
