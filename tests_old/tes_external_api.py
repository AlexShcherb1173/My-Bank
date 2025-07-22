import unittest
from unittest.mock import patch
from src_old.external_api import get_transaction_amount_rub


class TestTransactionConversion(unittest.TestCase):

    @patch("src.external_api.requests.get")
    def test_usd_conversion(self, mock_get):
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": {"RUB": 90.5}
        }

        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 9050.0)

    @patch("src.external_api.requests.get")
    def test_eur_conversion(self, mock_get):
        transaction = {
            "operationAmount": {
                "amount": "50",
                "currency": {"code": "EUR"}
            }
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": {"RUB": 100.0}
        }

        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 5000.0)

    def test_rub_conversion(self):
        transaction = {
            "operationAmount": {
                "amount": "1234.56",
                "currency": {"code": "RUB"}
            }
        }
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 1234.56)

    def test_invalid_amount(self):
        transaction = {
            "operationAmount": {
                "amount": "abc",
                "currency": {"code": "USD"}
            }
        }
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 0.0)
