import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch
from main import *
import pytest


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("Maestro1596837868705199", "Maestro1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет35383033474447895560", "Счет **5560"),
        ("VisaClassic6831982476737658", "VisaClassic6831 98** **** 7658"),
        ("Visa Platinum8990922113665229", "Visa Platinum8990 92** **** 5229"),
        ("VisaGold 5999414228426353", "VisaGold 5999 41** **** 6353"),
        ("счет  73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(str, exp_str):
    assert mask_account_card(str) == exp_str


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-06-30T02:", "30.06.2025"),
        ("2025-07-01", "01.07.2025"),
        ("2021-01-01rkuryflfkhfglf", "01.01.2021"),
    ],
)
def test_get_date(str, exp_str):
    assert get_date(str) == exp_str


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


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("1111222233334444", "1111 22** **** 4444"),
        ("4444333322221111", "4444 33** **** 1111"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("11112222333344445", "1111 22** **** 4444"),
        ("111122223333444", "1111 22** **** 444"),
        ("111abc22333344sd", "111a bc** **** 44sd"),
        ("111abc2244sd", "111a bc** **** "),
        ("", "   "),
    ],
)
def test_get_mask_card_number(str, exp_str):
    assert get_mask_card_number(str) == exp_str


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("1111222233334444", "**4444"),
        ("4444333322221111", "**1111"),
        ("1234567890123456", "**3456"),
        ("12345", "**2345"),
        ("12345678900987654321", "**4321"),
        ("1234567890098765aaaa", "**aaaa"),
        ("", "**"),
    ],
)
def test_get_mask_acount(str, exp_str):
    assert get_mask_acount(str) == exp_str


class TestReadJsonFile(unittest.TestCase):

    def test_valid_json_list_of_dicts(self):
        data = [{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, data)
        os.remove(f_path)

    def test_file_does_not_exist(self):
        result = read_json_file("nonexistent_file.json")
        self.assertEqual(result, [])

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_invalid_json_format(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("this is not json")
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_json_not_a_list(self):
        data = {"amount": 100}
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    def test_json_list_not_dicts(self):
        data = [1, 2, 3]
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            f_path = f.name

        result = read_json_file(f_path)
        self.assertEqual(result, [])
        os.remove(f_path)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]),
    )
    @patch("os.path.exists", return_value=True)
    def test_read_valid_json(self, mock_exists, mock_file):
        result = read_json_file("dummy_path.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)

    @patch("builtins.open", new_callable=mock_open, read_data="not json")
    @patch("os.path.exists", return_value=True)
    def test_read_invalid_json(self, mock_exists, mock_file):
        result = read_json_file("dummy_path.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=False)
    def test_file_not_exists(self, mock_exists):
        result = read_json_file("missing.json")
        self.assertEqual(result, [])

class TestReadTransactionsFromCSV(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="dummy")
    @patch("main.transform_transaction")
    @patch("csv.DictReader")
    def test_read_transactions_from_csv(self, mock_dict_reader, mock_transform, mock_file):
        # Подготавливаем фейковые строки, которые возвращает csv.DictReader
        fake_rows = [
            {
                "id;state;amount;currency_name;from;to": "650703;EXECUTED;16210;Sol;Счет 58803664561298323391;Счет 39745660563456619397"
            },
            {
                "id;state;amount;currency_name;from;to": "111111;EXECUTED;33333;Sol;Счет 58803664561298323391;Счет 39745660563456619397"
            },
        ]
        mock_dict_reader.return_value = fake_rows

        # Подготавливаем то, что должна вернуть transform_transaction
        mock_transform.side_effect = [
            {
                "id": 650703.0,
                "state": "EXECUTED",
                "amount": 16210.0,
                "currency_name": "Sol",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
            },
            {
                "id": 111111.0,
                "state": "EXECUTED",
                "amount": 33333.0,
                "currency_name": "Sol",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
            },
        ]

        result = read_transactions_from_csv("fake_path.csv")

        self.assertEqual(
            result,
            [
                {
                    "id": 650703.0,
                    "state": "EXECUTED",
                    "amount": 16210.0,
                    "currency_name": "Sol",
                    "from": "Счет 58803664561298323391",
                    "to": "Счет 39745660563456619397",
                },
                {
                    "id": 111111.0,
                    "state": "EXECUTED",
                    "amount": 33333.0,
                    "currency_name": "Sol",
                    "from": "Счет 58803664561298323391",
                    "to": "Счет 39745660563456619397",
                },
            ],
        )
        mock_file.assert_called_once_with("fake_path.csv", mode="r", encoding="utf-8")
        self.assertEqual(mock_transform.call_count, 2)

    os.chdir(r"/")

class TestReadTransactionsFromExcel(unittest.TestCase):
    @patch("main.pd.read_excel")
    def test_read_transactions_from_excel(self, mock_read_excel):
        # Подготовка фейкового DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("fake_path.xlsx")
        # Проверка
        self.assertEqual(result, [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
        mock_read_excel.assert_called_once_with("fake_path.xlsx")
        mock_df.to_dict.assert_called_once_with(orient="records")


class TestInputChoice(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    def test_valid_json_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "json")

    @patch("builtins.input", side_effect=["2"])
    def test_valid_csv_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "csv")

    @patch("builtins.input", side_effect=["3"])
    def test_valid_xlsx_choice(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "xlsx")

    @patch("builtins.input", side_effect=["0", "4", "abc", "", "2"])
    def test_invalid_then_valid_input(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "csv")

    @patch("builtins.input", side_effect=["abc", "!", "3"])
    def test_multiple_invalid_then_valid(self, mock_input):
        result = input_choice()
        self.assertEqual(result, "xlsx")

class TestInputSortDate(unittest.TestCase):
    @patch("builtins.input", side_effect=["Да", "по убыванию"])
    def test_sort_yes_descending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, True])

    @patch("builtins.input", side_effect=["Да", "по возрастанию"])
    def test_sort_yes_ascending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])

    @patch("builtins.input", side_effect=["Нет"])
    def test_sort_no(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [False])

    @patch("builtins.input", side_effect=["abc", "да", "убыванию"])
    def test_invalid_then_valid_descending(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, True])

    @patch("builtins.input", side_effect=["123", "Нет"])
    def test_invalid_then_valid_no(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [False])

    @patch("builtins.input", side_effect=["ДА", "ВОЗРАСТАНИЮ"])
    def test_upper_case_input(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])

    @patch("builtins.input", side_effect=["да", "сначала старые", "по возрастанию"])
    def test_invalid_sort_direction_then_valid(self, mock_input):
        result = input_sort_date()
        self.assertEqual(result, [True, False])


class TestInputSortCurrency(unittest.TestCase):

    @patch("builtins.input", side_effect=["Да"])
    def test_rub_currency_yes(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["Нет"])
    def test_rub_currency_no(self, mock_input):
        result = input_sort_currency()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["abc", "ДА"])
    def test_invalid_then_valid_uppercase_yes(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["123", "нет"])
    def test_invalid_numeric_then_valid_no(self, mock_input):
        result = input_sort_currency()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["", "что-то", "да"])
    def test_multiple_invalid_then_valid(self, mock_input):
        result = input_sort_currency()
        self.assertTrue(result)


class TestInputDescr(unittest.TestCase):

    @patch("builtins.input", side_effect=["Да"])
    def test_filter_yes(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["Нет"])
    def test_filter_no(self, mock_input):
        result = input_descr()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["ДА"])
    def test_uppercase_yes(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["нет"])
    def test_lowercase_no(self, mock_input):
        result = input_descr()
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["123", "abc", "Да"])
    def test_invalid_then_valid(self, mock_input):
        result = input_descr()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["", "нет"])
    def test_empty_then_valid(self, mock_input):
        result = input_descr()
        self.assertFalse(result)


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


class TestTransformTransactions(unittest.TestCase):

    def test_valid_transaction(self):
        input_data = [
            {
                "id": "123",
                "state": "EXECUTED",
                "date": "2023.01.01",
                "operationAmount": {"amount": "1000.50", "currency": {"name": "Russian Ruble", "code": "RUB"}},
                "description": "Payment",
                "from": "Account A",
                "to": "Account B",
            }
        ]
        result = transform_transactions(input_data)
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
                "operationAmount": {"amount": "1000.50", "currency": {"name": "RUB", "code": "RUB"}},
                "description": "Payment",
            }
        ]
        result = transform_transactions(input_data)
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
        result = transform_transactions(input_data)
        self.assertEqual(result, [])

    def test_missing_from_field(self):
        input_data = [
            {
                "id": "456",
                "state": "EXECUTED",
                "date": "2023.05.01",
                "operationAmount": {"amount": "200", "currency": {"name": "Dollar", "code": "USD"}},
                "description": "Transfer",
                "to": "Account C",
            }
        ]
        result = transform_transactions(input_data)
        self.assertEqual(result[0]["from"], "")

    def test_invalid_id_and_amount_types(self):
        input_data = [
            {
                "id": "not-a-number",
                "state": "EXECUTED",
                "date": "2023.01.01",
                "operationAmount": {"amount": "also-bad", "currency": {"name": "USD", "code": "USD"}},
                "description": "Broken",
                "to": "Account D",
            }
        ]
        result = transform_transactions(input_data)
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


class TestFormatTransactions(unittest.TestCase):

    @patch("main.get_date", return_value="01.01.2024")
    @patch("main.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
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

    @patch("main.get_date", return_value="15.07.2023")
    @patch("main.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
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

    @patch("main.get_date", return_value="")
    @patch("main.mask_account_card", return_value="")
    def test_empty_transaction(self, mock_mask, mock_date):
        transactions = [{}]
        expected_output = " \n\nСумма: 0 .\n"
        result = format_transactions(transactions)
        self.assertEqual(result.strip(), expected_output.strip())

    @patch("main.get_date", return_value="05.05.2025")
    @patch("main.mask_account_card", side_effect=lambda x: f"***{x[-4:]}" if x else "")
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


class TestMainRun(unittest.TestCase):

    @patch("main.os.chdir")
    @patch(
        "main.input",
        side_effect=[
            "json",  # input_choice
            "EXECUTED",  # input_state
            "да",
            "по убыванию",  # input_sort_date
            "да",  # input_sort_currency
            "да",
            "оплата",  # input_descr + слово
        ],
    )
    @patch("main.input_choice", return_value="json")
    @patch("main.input_state", return_value="EXECUTED")
    @patch("main.input_sort_date", return_value=[True, True])
    @patch("main.input_sort_currency", return_value=True)
    @patch("main.input_descr", return_value=True)
    @patch("main.read_json_file")
    @patch("main.transform_transactions")
    @patch("main.filter_by_state")
    @patch("main.sort_by_date")
    @patch("main.filter_and_sort_by_currency")
    @patch("main.process_bank_search")
    @patch("main.replace_nan_with_zero")
    @patch("main.format_transactions", return_value="Formatted Output")
    @patch("main.print")
    def test_full_run_json_flow(
        self,
        mock_print,
        mock_format,
        mock_replace,
        mock_process,
        mock_filter_currency,
        mock_sort_by_date,
        mock_filter_by_state,
        mock_transform,
        mock_read_json,
        mock_descr,
        mock_currency,
        mock_date,
        mock_state,
        mock_choice,
        mock_input,
        mock_chdir,
    ):
        # Подготовка фейковых данных на каждом этапе
        mock_read_json.return_value = [{"id": 1}]
        mock_transform.return_value = [{"id": 1}]
        mock_filter_by_state.return_value = [{"id": 1}]
        mock_sort_by_date.return_value = [{"id": 1}]
        mock_filter_currency.return_value = [{"id": 1}]
        mock_process.return_value = [{"id": 1}]
        mock_replace.return_value = [{"id": 1}]

        run()

        mock_print.assert_any_call("для обработки выбран json файл")
        mock_print.assert_any_call("Всего банковских операций в выборке 1\n")
        mock_print.assert_any_call("Formatted Output")
