import unittest
from unittest.mock import patch

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

        from your_module import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "налога")

        mock_compile.assert_called_once_with(r'\bналога\b', re.IGNORECASE)
        self.assertEqual(len(result), 2)
        self.assertTrue(all("налога" in item["description"] for item in result))

    def test_search_actual_behavior(self):
        from your_module import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "налога")
        self.assertEqual(len(result), 2)
        self.assertEqual({r["id"] for r in result}, {1, 3})

    def test_no_matches(self):
        from your_module import process_bank_search  # замените на реальный путь
        result = process_bank_search(self.data, "кредит")
        self.assertEqual(result, [])

import unittest
from unittest.mock import patch, MagicMock

class TestProcessBankOperations(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"id": 1, "description": "Оплата налогов"},
            {"id": 2, "description": "Оплата налогов"},
            {"id": 3, "description": "Снятие наличных"},
        ]
        self.categories = ["Оплата налогов", "Снятие наличных", "Перевод"]

    @patch("collections.Counter")
    def test_counter_called_with_descriptions(self, mock_counter):
        mock_counter.return_value = {"Оплата налогов": 2, "Снятие наличных": 1}
        from your_module import process_bank_operations  # замените на ваш путь
        result = process_bank_operations(self.data, self.categories)
        mock_counter.assert_called_once_with([
            "Оплата налогов",
            "Оплата налогов",
            "Снятие наличных"
        ])
        self.assertEqual(result["Оплата налогов"], 2)
        self.assertEqual(result["Снятие наличных"], 1)
        self.assertEqual(result["Перевод"], 0)

    def test_actual_behavior(self):
        from your_module import process_bank_operations  # замените на ваш путь
        result = process_bank_operations(self.data, self.categories)
        expected = {
            "Оплата налогов": 2,
            "Снятие наличных": 1,
            "Перевод": 0
        }
        self.assertEqual(result, expected)