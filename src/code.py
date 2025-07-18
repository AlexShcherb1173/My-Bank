# import traceback
# from decorators import *
from utils import *

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
transactions = read_json_file('operations.json')
print(transactions)