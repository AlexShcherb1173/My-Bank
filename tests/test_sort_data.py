import unittest
from sort_data import *


def test_filter_by_state(list_dict2):
    assert filter_by_state(list_dict2) == [
        {"": 41428829, "state": "EXECUTED", "": "2019-07-03T18:35:29.512364"},
        {"": 939719570, "state": "EXECUTED", "": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state(list_dict3):
    assert filter_by_state(list_dict3) == [{"": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]


def test_filter_by_state(list_dict4):
    assert filter_by_state(list_dict4) == [
        {"id": null, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state(list_dict6):
    assert filter_by_state(list_dict6) == [
        {"": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

class TestFilterAndSortByCurrency(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            {"id": 1, "amount": 100, "currency_code": "RUB"},
            {"id": 2, "amount": 200, "currency_code": "USD"},
            {"id": 3, "amount": 300, "currency_code": "RUB"},
            {"id": 4, "amount": 400, "currency_code": "EUR"},
            {"id": 5, "amount": 500, "currency_code": "RUB"},
        ]

    def test_filter_rub(self):
        result = filter_and_sort_by_currency(self.transactions, "RUB")
        expected = [
            {"id": 1, "amount": 100, "currency_code": "RUB"},
            {"id": 3, "amount": 300, "currency_code": "RUB"},
            {"id": 5, "amount": 500, "currency_code": "RUB"},
        ]
        self.assertEqual(result, expected)

    def test_filter_usd(self):
        result = filter_and_sort_by_currency(self.transactions, "USD")
        expected = [
            {"id": 2, "amount": 200, "currency_code": "USD"},
        ]
        self.assertEqual(result, expected)

    def test_filter_eur(self):
        result = filter_and_sort_by_currency(self.transactions, "EUR")
        expected = [
            {"id": 4, "amount": 400, "currency_code": "EUR"},
        ]
        self.assertEqual(result, expected)

    def test_filter_not_found(self):
        result = filter_and_sort_by_currency(self.transactions, "JPY")
        self.assertEqual(result, [])

    def test_empty_transaction_list(self):
        result = filter_and_sort_by_currency([], "RUB")
        self.assertEqual(result, [])

class TestProcessBankSearch(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"id": 1, "description": "Оплата товара"},
            {"id": 2, "description": "Перевод в рублях"},
            {"id": 3, "description": "Снятие наличных"},
            {"id": 4, "description": "Оплата услуг"},
            {"id": 5, "description": "переВОД на карту"},
            {"id": 6, "description": "Наличные переведены"},
            {"id": 7, "description": ""},
            {"id": 8},  # description отсутствует
        ]

    def test_exact_word_match_case_insensitive(self):
        result = process_bank_search(self.data, "оплата")
        self.assertEqual([r["id"] for r in result], [1, 4])

    def test_match_with_different_case(self):
        result = process_bank_search(self.data, "перевод")
        self.assertEqual([r["id"] for r in result], [2, 5])

    def test_no_matches(self):
        result = process_bank_search(self.data, "кредит")
        self.assertEqual(result, [])

    def test_partial_word_should_not_match(self):
        # "наличные переведены" — слово "перевод" внутри "переведены" НЕ должно совпасть
        result = process_bank_search(self.data, "перевод")
        ids = [r["id"] for r in result]
        self.assertNotIn(6, ids)  # id=6 не должен быть в списке

    def test_empty_description_fields(self):
        result = process_bank_search(self.data, "перевод")
        ids = [r["id"] for r in result]
        self.assertNotIn(7, ids)
        self.assertNotIn(8, ids)

    def test_search_with_special_regex_chars(self):
        # Проверка, что специальные символы экранируются (например, "+")
        data = [{"id": 1, "description": "Оплата+товар"}]
        result = process_bank_search(data, "Оплата+товар")
        self.assertEqual(len(result), 1)

class TestSortByDate(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"id": 1, "state": "EXECUTED", "date": "2023-05-01T10:00:00Z"},
            {"id": 2, "state": "EXECUTED", "date": "2023-04-01T10:00:00Z"},
            {"id": 3, "state": "EXECUTED", "date": "2023-06-01T10:00:00Z"}
        ]

    def test_sort_descending_by_default(self):
        result = sort_by_date(self.data)
        self.assertEqual([r["id"] for r in result], [3, 1, 2])

    def test_sort_ascending(self):
        result = sort_by_date(self.data, reverse=False)
        self.assertEqual([r["id"] for r in result], [2, 1, 3])

    def test_empty_list(self):
        result = sort_by_date([])
        self.assertEqual(result, [])

    def test_same_dates(self):
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2023-05-01T10:00:00Z"},
            {"id": 2, "state": "EXECUTED", "date": "2023-05-01T10:00:00Z"},
        ]
        result = sort_by_date(data)
        self.assertEqual([r["id"] for r in result], [1, 2])  # Порядок сохранится

    def test_sort_stable(self):
        # Проверим стабильность сортировки (если даты равны, порядок сохраняется)
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2023-05-01T10:00:00Z"},
            {"id": 2, "state": "EXECUTED", "date": "2023-05-01T10:00:00Z"},
            {"id": 3, "state": "EXECUTED", "date": "2023-04-01T10:00:00Z"}
        ]
        result = sort_by_date(data, reverse=False)
        self.assertEqual([r["id"] for r in result], [3, 1, 2])


