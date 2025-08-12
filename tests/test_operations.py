import unittest
from unittest.mock import patch, MagicMock
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


class TestProcessBankOperations(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {
                "id": 1,
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
                "id": 2,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту"
            },
            {
                "id": 3,
                "description": "Перевод организации"
            }
        ]
        self.categories = ["Перевод организации", "Перевод с карты на карту"]

    def test_correct_counting(self):
        result = process_bank_operations(self.sample_data, self.categories)
        expected = {
            "Перевод организации": 2,
            "Перевод с карты на карту": 1
        }
        self.assertEqual(result, expected)

    def test_empty_input(self):
        result = process_bank_operations([], self.categories)
        self.assertEqual(result, {})

    def test_no_matching_categories(self):
        result = process_bank_operations(self.sample_data, ["Несуществующая категория"])
        self.assertEqual(result, {})

    @patch("operations.Counter")
    def test_counter_called_properly(self, mock_counter_class):
        mock_counter_instance = MagicMock()
        mock_counter_class.return_value = mock_counter_instance

        mock_counter_instance.__setitem__.side_effect = lambda key, value: None
        mock_counter_instance.__getitem__.side_effect = lambda key: 0

        # вызов функции
        process_bank_operations(self.sample_data, self.categories)

        # проверка, что Counter был создан
        mock_counter_class.assert_called_once()
        # проверка, что ключи, которые входят в категории, увеличивались
        self.assertTrue(mock_counter_instance.__setitem__.called or mock_counter_instance.__getitem__.called)

