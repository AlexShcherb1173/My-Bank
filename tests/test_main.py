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

    os.chdir(r"/")

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    os.chdir(r"/")

    class TestReadTransactionsFromCSV(unittest.TestCase):
        @patch("builtins.open", new_callable=mock_open, read_data="dummy")
        @patch("freader.transform_transaction")
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
            self.assertEqual(mock_transform.call_count, 0)

    os.chdir(r"/")

    class TestReadTransactionsFromExcel(unittest.TestCase):
        @patch("freader.pd.read_excel")
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
