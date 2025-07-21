# import traceback
# from decorators import *

# LOG_FILE = "test_log.txt"
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

import json
import os
import logging
from utils_new import *

if __name__ == "__main__":
    data = read_json_file(r"data\operations.json")
    print(data)