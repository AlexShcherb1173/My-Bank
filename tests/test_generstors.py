import pytest
from src.generators import *


@pytest.mark.parametrize(
    "start, stop, exp_str",
    [
        ("1", "1", "0000 0000 0000 0001"),
        ("1111111111111111", "1111111111111111", "1111 1111 1111 1111"),
        ("9999999999999999", "9999999999999999", "9999 9999 9999 9999"),
        ("1111222233334444", "1111222233334444", "1111 2222 3333 4444"),
        ("123456789012345", "123456789012345", "0123 4567 8901 2345"),
    ],
)
def test_card_number_generator(start, stop, exp_str):
    assert list(card_number_generator(start, stop))[0] == exp_str


def test_filter_by_currency(transactions1):
    usd_transactions = filter_by_currency(transactions1, "USD")
    assert list(usd_transactions)[0] == (
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    )


def test_filter_by_currency(transactions2):
    usd_transactions = filter_by_currency(transactions2, "EUR")
    assert list(usd_transactions)[0] == (
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    )


def test_transaction_descriptions(transactions1):
    name_transactions = transaction_descriptions(transactions1)
    assert list(name_transactions)[0] == "Перевод организации"


def test_transaction_descriptions(transactions2):
    name_transactions = transaction_descriptions(transactions2)
    assert list(name_transactions)[2] == "Перевод со счета на счет"


def test_transaction_descriptions(transactions3):
    name_transactions = transaction_descriptions(transactions3)
    assert list(name_transactions)[0] == "Перевод с карты на карту"
