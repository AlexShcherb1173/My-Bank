import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch
from main import *



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
