import csv
import pandas as pd
import json
import os


def read_json_file(filepath: str) -> list:
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        return []


def transform_transaction(input_dict: dict) -> dict:
    """Функция преобразования формата списка словарей из csv в классический вид"""
    # Извлекаем единственный ключ и значение
    full_header, full_values = list(input_dict.items())[0]

    # Разделяем заголовки и значения по символу ";"
    keys = full_header.split(";")
    values = full_values.split(";")

    # Преобразуем значения
    transformed_values = []
    for key, value in zip(keys, values):
        if key in ("id", "amount"):
            if value.isdigit():
                fvalue = float(value)
                # print(fvalue, type(fvalue))
                transformed_values.append(fvalue)
        else:
            transformed_values.append(value)

    # Создаем словарь из ключей и преобразованных значений
    return dict(zip(keys, transformed_values))


def read_transactions_from_csv(file_path: str) -> list[dict]:
    """функция для считывания финансовых операций из CSV.
    Принимает путь к файлу CSV в качестве аргумента.
    Выдает список словарей с транзакциями."""
    transactions = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transaction = transform_transaction(row)
            transactions.append(transaction)
    return transactions


def read_transactions_from_excel(file_path: str) -> list[dict]:
    """Функция для считывания финансовых операций из Excel.
    Принимает путь к файлу Excel в качестве аргумента.
    Выдает список словарей с транзакциями."""
    df = pd.read_excel(file_path)
    transactions = df.to_dict(orient="records")
    return transactions

def filter_by_state(list_dict: list[dict], state_in: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей-выборку по полю state"""
    list_dict_filer_state = []
    for account in list_dict:
        if account['state'] == state_in:
            list_dict_filer_state.append(account)
    return list_dict_filer_state


def sort_by_date(list_dict: list[dict], reverse: bool = True) -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей сортированных по date(назад или вперед)"""
    if reverse:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=True)
    else:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=False)
    return list_dict_sort_by_date


def input_choice():
    inp = input('''Привет! Добро пожаловать в программу работы с банковскими транзакциями.
    Выберите необходимый пункт меню:
      1. Получить информацию о транзакциях из JSON-файла
      2. Получить информацию о транзакциях из CSV-файла
      3. Получить информацию о транзакциях из XLSX-файла \n''')
    while True:
        if inp.isdigit():
            i = int(inp)
            if i == 1:
                ch = 'json'
                break
            elif i == 2:
                ch = 'csv'
                break
            elif i == 3:
                ch = "xlsx"
                break
            else:
                print('неправильный ввод, сделайте правильный выбор')
                inp = input()
        else:
            print('неправильный ввод, сделайте правильный выбор')
            inp = input()
    return ch

os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
filepath_json = r'data\operations1.json'
filepath_csv = r'data\transactions.csv'
filepath_xlsx = r'data\transactions_excel.xlsx'

choice = input_choice()
print (f"для обработки выбран {choice} файл")
if choice == 'json':
    transaction_table = read_json_file(filepath_json)
elif choice == 'csv':
    transaction_table = read_transactions_from_csv(filepath_csv)
elif choice == 'xlsx':
    transaction_table = read_transactions_from_excel(filepath_xlsx)

def input_state():
    inp = input('''Введите статус, по которому необходимо выполнить фильтрацию. \n
    Доступные cтатусы: EXECUTED, CANCELED, PENDING \n''')
    while True:
        if inp.isalpha():
            i = inp.upper()
            if i == 'EXECUTED':
                st = 'EXECUTED'
                break
            elif i == 'CANCELED':
                st = 'CANCELED'
                break
            elif i == 'PENDING':
                st = 'PENDING'
                break
            else:
                print(f'Статус операции {inp} недоступен, сделайте правильный выбор')
                inp = input()
        else:
            print(f'Статус операции {inp} недоступен, сделайте правильный выбор')
            inp = input()
    return st
f_state_trans_tab = filter_by_state(transaction_table , input_state())
print(f_state_trans_tab)
#     = input('''Введите статус, по которому необходимо выполнить фильтрацию. \n
# Доступные cтатусы: EXECUTED, CANCELED, PENDING''')
# f_st = input()
# if f_st.isalpha():
#     f_state= f_st.lower()
# else:

