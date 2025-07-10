import pytest
from generators import filter_by_currency
from generators import transaction_descriptions
from generators import card_number_generator
# def filter_by_currency(transactions:list[dict], currency:str):
#     """функция, которая принимает на вход список словарей, представляющих транзакции возвращает итератор,
#        который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD)."""
#     for i in transactions:
#         if i["operationAmount"]["currency"]["code"] == currency:
#             yield i
#
# def transaction_descriptions(transaction_des: list[dict]) -> Iterable:
#     """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
#     for transaction in transaction_des:
#         yield transaction.get("description")
#
# def card_number_generator(start: str = '1', stop: str = '9999999999999999') -> str:
#     for num in range(int(start), int(stop)+1):
#         yield '{:04d} {:04d} {:04d} {:04d}'.format(num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4)

@pytest.mark.parametrize(
    "start, stop, exp_str",
    [
        ('1', '1', '0000 0000 0000 0001'),
        ('1111111111111111', '1111111111111111', '1111 1111 1111 1111'),
        ('9999999999999999', '9999999999999999', '9999 9999 9999 9999'),
        ('1111222233334444', '1111222233334444', '1111 2222 3333 4444'),
        ('123456789012345', '123456789012345', '0123 4567 8901 2345'),
    ],
)

def test_card_number_generator(start, stop, exp_str):
    assert list(generators.card_number_generator(start, stop))[0] == exp_str


def test_filter_by_currency(transactions1):
     usd_transactions = generators.filter_by_currency(transactions1, "USD")
     assert list(usd_transactions)[0] == ({"id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702" })


def test_filter_by_currency(transactions2):
    usd_transactions = generators.filter_by_currency(transactions2, "EUR")
    assert list(usd_transactions)[0] == ({"id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702" })


def test_transaction_descriptions(transactions1):
    name_transactions = generators.transaction_descriptions(transactions1)
    assert list(name_transactions)[0] == "Перевод организации"

def test_transaction_descriptions(transactions2):
    name_transactions = generators.transaction_descriptions(transactions2)
    assert list(name_transactions)[2] == "Перевод со счета на счет"

def test_transaction_descriptions(transactions3):
    name_transactions = generators.transaction_descriptions(transactions3)
    assert list(name_transactions)[0] == "Перевод с карты на карту"


