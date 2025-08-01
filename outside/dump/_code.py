# import traceback
# from decorators import *

# LOG_FILE = "_test_log.txt"
#
# @log()
# def add(a, b):
#     return a + b
#
# @log()
# def fail_func(a, b):
#     return a / b  # Возможна ZeroDivisionError
#
# @log(filename=LOG_FILE)
# def multiply(x, y):
#     return x * y
#
# @log(filename=LOG_FILE)
# def crash(x):
#     raise ValueError("something went wrong")
import json
import os
def read_json_file(filepath: str) -> list:
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список."""
    print(filepath)
    if not os.path.exists(filepath):
        return [1]

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                return [2]
    except (json.JSONDecodeError, IOError):
        return [3]
os.chdir(r'/')
filepath_json = r'data\operations.json'
print(read_json_file(filepath_json))
# === Точка входа для запуска вручную ===
# if __name__ == "__main__":
#     print("Ручной запуск функций:")
#     add(1, 2)
#     try:
#         fail_func(1, 0)
#     except Exception:
#         pass
#     multiply(3, 3)
#     try:
#         crash(5)
#     except Exception:
#         pass
# if __name__ == '__main__':
#     unittest.main()
# transactions = read_json_file('operations.json')
# print(transactions)

# from masks import get_mask_card_number, get_mask_acount
#
# print(get_mask_card_number("1234567812345678"))
# print(get_mask_acount("40817810099910004312"))
# print(get_mask_card_number("abc"))           # вызовет ошибку
# print(get_mask_acount("12"))                 # вызовет ошибку

# from src_old.utils_new import *
#
# if __name__ == "__main__":
#     data = read_json_file(r"data\operations.json")
#     print(data)

# sample_data = [
#     {
#         "id": 650703,
#         "state": "EXECUTED",
#         "date": "2023-09-05T11:30:32Z",
#         "amount": 16210,
#         "currency_name": "Sol",
#         "currency_code": "PEN",
#         "from": "Счет 58803664561298323391",
#         "to": "Счет 39745660563456619397",
#         "description": "Перевод организации"
#     },
#     {
#         "id": 3598919,
#         "state": "EXECUTED",
#         "date": "2020-12-06T23:00:58Z",
#         "amount": 29740,
#         "currency_name": "Peso",
#         "currency_code": "COP",
#         "from": "Discover 3172601889670065",
#         "to": "Discover 0720428384694643",
#         "description": "Перевод с карты на карту"
#     },
# ]
#
# sample_data1 = [
#     {
#         "id": 1,
#         "description": "Перевод организации"
#     },
#     {
#         "id": 2,
#         "description": "Перевод с карты на карту"
#     },
#     {
#         "id": 3,
#         "description": "Перевод с карты на карту"
#     },
#     {
#         "id": 4,
#         "description": "Оплата услуг"
#     }
# ]
# categories = ["Перевод с карты на карту", "Оплата услуг", "Снятие наличных"]
# # Ожидаемый результат:
# # {
# #     "Перевод с карты на карту": 2,
# #     "Оплата услуг": 1,
# #     "Снятие наличных": 0
# # }
#
# from operations import *
# import os
from deepdiff import DeepDiff

#print(process_bank_search(sample_data, ''))
# print(process_bank_operations(sample_data1, categories))
#
# os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
# print ('Excel')
# print(read_transactions_from_excel(r'data\transactions_excel.xlsx'))
# print('\n')
# print('csv')
# print(read_transactions_from_csv(r'data\transactions.csv'))
# print('\n')
# print(read_transactions_from_excel(r'data\transactions_excel.xlsx') == read_transactions_from_csv(r'data\transactions.csv'))
# list1 = read_transactions_from_excel(r'data\transactions_excel.xlsx')
#
# list2 = read_transactions_from_csv(r'data\transactions.csv')
#
# diff = DeepDiff(list1, list2, ignore_order=True)
# print(diff)

#print(transform_transaction({'id;state;date;amount;currency_name;currency_code;from;to;description': '650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации'}))