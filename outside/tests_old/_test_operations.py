import unittest
from unittest.mock import patch
from operations import *

class TestProcessBankSearch(unittest.TestCase):

    def setUp(self):
        self.data = [
            {
                "id": 1,
                "description": "Оплата налога"
            },
            {
                "id": 2,
                "description": "Перевод на карту"
            },
            {
                "id": 3,
                "description": "Возврат налога"
            },
        ]

    @patch("re.compile")
    def test_search_calls_re_compile(self, mock_compile):
        mock_pattern = mock_compile.return_value
        mock_pattern.search.side_effect = lambda x: "налога" in x

        from operations import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "налога")

        mock_compile.assert_called_once_with(r'\bналога\b', re.IGNORECASE)
        self.assertEqual(len(result), 2)
        self.assertTrue(all("налога" in item["description"] for item in result))

    def test_search_actual_behavior(self):
        from operations import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "налога")
        self.assertEqual(len(result), 2)
        self.assertEqual({r["id"] for r in result}, {1, 3})

    def test_no_matches(self):
        from operations import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "кредит")
        self.assertEqual(result, [])

sample_data = [
    {
        "id": 650703,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": 16210,
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации"
    },
    {
        "id": 3598919,
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "amount": 29740,
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "Discover 3172601889670065",
        "to": "Discover 0720428384694643",
        "description": "Перевод с карты на карту"
    },
]

# Тесты
class TestProcessBankOperations(unittest.TestCase):

    def test_single_category_match(self):
        categories = ["организации"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"организации": 1})

    def test_multiple_category_matches(self):
        categories = ["перевод", "карты"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"перевод": 2, "карты": 1})

    def test_no_matches(self):
        categories = ["покупка", "снятие"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"покупка": 0, "снятие": 0})

    def test_case_insensitive_matching(self):
        categories = ["ОрГаНиЗаЦиИ", "ПЕРЕВОД"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"ОрГаНиЗаЦиИ": 1, "ПЕРЕВОД": 2})

    def test_empty_description(self):
        test_data = sample_data + [{"description": ""}]
        categories = ["перевод"]
        result = process_bank_operations(test_data, categories)
        self.assertEqual(result, {"перевод": 2})  # Пустая строка не добавляет счёт

    def test_empty_categories(self):
        result = process_bank_operations(sample_data, [])
        self.assertEqual(result, {})

    def test_empty_data(self):
        categories = ["перевод"]
        result = process_bank_operations([], categories)
        self.assertEqual(result, {"перевод": 0})
class TestProcessBankOperations(unittest.TestCase):

    def test_single_category_match(self):
        categories = ["организации"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"организации": 1})

    def test_multiple_category_matches(self):
        categories = ["перевод", "карты"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"перевод": 2, "карты": 1})

    def test_no_matches(self):
        categories = ["покупка", "снятие"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"покупка": 0, "снятие": 0})

    def test_case_insensitive_matching(self):
        categories = ["ОрГаНиЗаЦиИ", "ПЕРЕВОД"]
        result = process_bank_operations(sample_data, categories)
        self.assertEqual(result, {"ОрГаНиЗаЦиИ": 1, "ПЕРЕВОД": 2})

    def test_empty_description(self):
        test_data = sample_data + [{"description": ""}]
        categories = ["перевод"]
        result = process_bank_operations(test_data, categories)
        self.assertEqual(result, {"перевод": 2})  # Пустая строка не добавляет счёт

    def test_empty_categories(self):
        result = process_bank_operations(sample_data, [])
        self.assertEqual(result, {})

    def test_empty_data(self):
        categories = ["перевод"]
        result = process_bank_operations([], categories)
        self.assertEqual(result, {"перевод": 0})