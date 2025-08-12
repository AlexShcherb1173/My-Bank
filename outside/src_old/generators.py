from typing import Iterable


def filter_by_currency(transactions: list[dict], currency: str) -> Iterable:
    """функция, которая принимает на вход список словарей, представляющих транзакции возвращает итератор,
    который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD)."""
    for i in transactions:
        if i["operationAmount"]["currency"]["tests"] == currency:
            yield i


def transaction_descriptions(transaction_des: list[dict]) -> Iterable:
    """Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
    for transaction in transaction_des:
        yield transaction.get("description")


def card_number_generator(start: str = "1", stop: str = "9999999999999999") -> Iterable:
    """Функция, которая выдает номера банковских карт в формате XXXX XXXX XXXX XXXX. Может генерировать номера карт
    в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999. Принимает начальное и конечное значения
    для генерации диапазона номеров."""
    for num in range(int(start), int(stop) + 1):
        yield "{:04d} {:04d} {:04d} {:04d}".format(
            num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4
        )
