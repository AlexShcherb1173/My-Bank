import csv
import json
import math
import os
import re
from typing import Any, Dict, List

import pandas as pd


# ---------------------------------masks---------------------------------------------------------------------------------
def get_mask_card_number(card_num_in: str) -> str:
    """Функция принимает строку с 16 цифрами номера карты и вовращает строку маску номера карты
    по 4 цифры через пробел, с 6й по 12ю цифру замена на *"""
    card_num_mask = ""
    for i in range(len(card_num_in)):
        if i > 5 and i < 12:
            card_num_mask += "*"
        else:
            card_num_mask += card_num_in[i]
    substring_1 = card_num_mask[:4]
    substring_2 = card_num_mask[4:8]
    substring_3 = card_num_mask[8:12]
    substring_4 = card_num_mask[12:16]
    card_num_mask = substring_1 + " " + substring_2 + " " + substring_3 + " " + substring_4
    return card_num_mask


def get_mask_acount(acount_num_in: str) -> str:
    """Функция принимает строку с цифрами номера счета и вовращает строку маску номера счета
    последние 4 цифры и две * перед ними"""
    acount_num_mask = "**"
    acount_num_mask += acount_num_in[-4:]
    return acount_num_mask


# ------------------------------widget-----------------------------------------------------------------------------------
def mask_account_card(card_account_number: str) -> Any:
    """Функция принимает строку с названием и номером карты или счета и возвращает строку соответсnвующей
    маски номера карты или счета"""
    substring = card_account_number[:4]
    substring = substring.lower()
    card_acc_num_mask = ""
    if substring == "счет":
        card_acc_num_mask = "Счет " + get_mask_acount(card_account_number[5:])
    else:
        account_num = ""
        prefics = ""
        for symbol in card_account_number:
            if symbol.isdigit():
                account_num += symbol
            elif symbol.isalpha():
                prefics += symbol
            elif symbol == " ":
                prefics += symbol
            card_acc_num_mask = prefics + get_mask_card_number(account_num)
    # print(card_acc_num_mask)
    return card_acc_num_mask


def get_date(date_time_in: str) -> str:
    """Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг"""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form


# -----------------------utils----------------------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------------------------------------------------
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


# --------------------------freader--------------------------------------------------------------------------------------
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


# ---------------------------------processing----------------------------------------------------------------------------
def filter_by_state(list_dict: list[dict], state_in: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей-выборку по полю state"""
    list_dict_filer_state = []
    for account in list_dict:
        # print(account)
        if account["state"] == state_in:
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


# -------------------------------input function-----------------------------------------------------------------------
def input_choice() -> str:
    """функция ввода выбора типа файла с защитой от неправильного ввода"""
    inp = input(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
    Выберите необходимый пункт меню:
      1. Получить информацию о транзакциях из JSON-файла
      2. Получить информацию о транзакциях из CSV-файла
      3. Получить информацию о транзакциях из XLSX-файла \n"""
    )
    while True:
        if inp.isdigit():
            i = int(inp)
            if i == 1:
                ch = "json"
                break
            elif i == 2:
                ch = "csv"
                break
            elif i == 3:
                ch = "xlsx"
                break
            else:
                print("неправильный ввод, сделайте правильный выбор")
                inp = input()
        else:
            print("неправильный ввод, сделайте правильный выбор")
            inp = input()
    return ch


def input_state() -> str:
    """функция ввода выбора статуса операции с защитой от неправильного ввода"""
    inp = input(
        """Введите статус, по которому необходимо выполнить фильтрацию.
      Доступные cтатусы: EXECUTED, CANCELED, PENDING\n"""
    )
    while True:
        if inp.isalpha():
            i = inp.upper()
            if i == "EXECUTED":
                st = "EXECUTED"
                break
            elif i == "CANCELED":
                st = "CANCELED"
                break
            elif i == "PENDING":
                st = "PENDING"
                break
            else:
                print(f"Статус операции {inp} недоступен, сделайте правильный выбор")
                inp = input()
        else:
            print(f"Статус операции {inp} недоступен, сделайте правильный выбор")
            inp = input()
    return st


def input_sort_date() -> list:
    """функция выбора сортировки даты с защитой от неправильного ввода"""
    st = []
    inp = input("""Отсортировать операции по дате? Да/Нет \n""")
    while True:
        if inp.isalpha():
            i = inp.lower()
            if i == "да":
                st.append(True)
                break
            elif i == "нет":
                st.append(False)
                break
            else:
                print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
                inp = input()
        else:
            print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
            inp = input()
    if st[0]:
        inp = input("""Отсортировать по возрастанию или по убыванию? \n""")
        while True:
            inp_l = inp.lower()
            index_1 = inp_l.find("возрастанию")
            index_2 = inp_l.find("убыванию")
            if index_1 != -1:
                st.append(False)
                break
            elif index_2 != -1:
                st.append(True)
                break
            else:
                print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
                inp = input()
    return st


def input_sort_currency() -> bool:
    """функция выбора сортировки вида валюты с защитой от неправильного ввода"""
    inp = input("""Выводить только рублевые транзакции? Да/Нет \n""")
    while True:
        if inp.isalpha():
            i = inp.lower()
            if i == "да":
                st = True
                break
            elif i == "нет":
                st = False
                break
            else:
                print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
                inp = input()
        else:
            print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
            inp = input()
    return st


def input_descr() -> bool:
    """функция выбора фильтрации по описанию с защитой от неправильного ввода"""
    inp = input("""Отфильтровать список транзакций по определенному слову в описании? Да/Нет \n""")
    while True:
        if inp.isalpha():
            i = inp.lower()
            if i == "да":
                st = True
                break
            elif i == "нет":
                st = False
                break
            else:
                print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
                inp = input()
        else:
            print(f"Ошибочный ввод, {inp} недоступен, сделайте правильный выбор")
            inp = input()
    return st


# -----------------------------------new function---------------------------------------------------------------------
def filter_and_sort_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Принимает список транзакций и код валюты.
    Возвращает отсортированный список транзакций, в которых currency_code совпадает."""
    filtered = [tx for tx in transactions if tx.get("currency_code") == currency_code]
    sorted_filtered = sorted(filtered, key=lambda tx: tx["currency_code"])
    return sorted_filtered


def transform_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """функция, которая преобразует список словарей из формата json файла в формат, совместимый с
    csv и xlsx файлами. С проверкой наличия необходимых ключей и отбрасыванием некорректных записей"""
    transformed = []
    for tx in transactions:
        if not isinstance(tx, dict):
            continue  # Пропускаем не-словарные записи
        required_keys = ["id", "state", "date", "operationAmount", "description", "to"]
        if not all(key in tx for key in required_keys):
            continue  # Пропускаем записи с отсутствующими ключами
        try:
            transformed_tx = {
                "id": float(tx["id"]),
                "state": tx["state"],
                "date": tx["date"].split(".")[0] + "Z",
                "amount": float(tx["operationAmount"]["amount"]),
                "currency_name": tx["operationAmount"]["currency"]["name"],
                "currency_code": tx["operationAmount"]["currency"]["code"],
                "from": tx.get("from", ""),
                "to": tx["to"],
                "description": tx["description"],
            }
            transformed.append(transformed_tx)

        except (KeyError, TypeError, ValueError) as e:
            print(f"Пропущена запись из-за ошибки: {e}\nЗапись: {tx}")
            continue
    return transformed


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Возвращает список словарей, где поле 'description' содержит искомую строку (поиск нечувствителен к регистру)."""
    pattern = re.compile(rf"\b{re.escape(search)}\b", re.IGNORECASE)
    return [entry for entry in data if pattern.search(entry.get("description", ""))]


def replace_nan_with_zero(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """функция для замены NaN значений в полях списков словарей транзакций на строку 0 для корректной обработки"""
    cleaned = []
    for tx in transactions:
        new_tx = {}
        for key, value in tx.items():
            if isinstance(value, float) and math.isnan(value):
                new_tx[key] = "0"
            else:
                new_tx[key] = value
        cleaned.append(new_tx)
    return cleaned


def format_transactions(transactions: List[Dict]) -> str:
    """функция преобразования списка словарей с транзакциями в читабельный текст"""
    result = []
    for tx in transactions:
        date = get_date(tx.get("date", ""))
        description = tx.get("description", "")
        sender = mask_account_card(tx.get("from", ""))
        receiver = mask_account_card(tx.get("to", ""))
        amount = tx.get("amount", 0)
        currency = tx.get("currency_name", "").strip()
        # Определяем, нужно ли вставлять стрелку
        if sender and receiver and sender != receiver:
            from_to = f"{sender} -> {receiver}"
        else:
            from_to = receiver  # только получатель, например, при открытии вклада
        block = f"{date} {description}\n{from_to}\nСумма: {amount} {currency}.\n"
        result.append(block)
    return "\n".join(result)


# ____________________________основной код обернутый в функцию ----------------------------------------------------
def main() -> None:
    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    # пути к тестовым файлам
    filepath_json = r"data\operations.json"
    filepath_csv = r"data\transactions.csv"
    filepath_xlsx = r"data\transactions_excel.xlsx"

    # ввод типа файлов данных
    choice = input_choice()
    print(f"для обработки выбран {choice} файл")

    # загрузка соответствующего файла в таблицу транзакций
    if choice == "json":
        transaction_table_json = read_json_file(filepath_json)
        transaction_table = transform_transactions(transaction_table_json)
    elif choice == "csv":
        transaction_table = read_transactions_from_csv(filepath_csv)
    elif choice == "xlsx":
        transaction_table = read_transactions_from_excel(filepath_xlsx)

    # фильтрация по категории
    f_state_transac_tab = filter_by_state(transaction_table, input_state())

    # фильтрация по дате по запросу
    date_param = input_sort_date()
    if date_param[0]:
        f_state_date_transac_tab = sort_by_date(f_state_transac_tab, date_param[1])
    else:
        f_state_date_transac_tab = f_state_transac_tab

    # фильтрация рублевых транзакций по запросу
    if input_sort_currency():
        f_state_date_currency_tab = filter_and_sort_by_currency(f_state_date_transac_tab, "RUB")
    else:
        f_state_date_currency_tab = f_state_date_transac_tab

    # фильтрация по описанию по запросу
    if input_descr():
        f_state_date_currency_descr_tab = process_bank_search(
            f_state_date_currency_tab, input("Введите слово для поиска: \n")
        )
    else:
        f_state_date_currency_descr_tab = f_state_date_currency_tab

    # очистка таблицы от пустых записей
    f_state_date_currency_descr_tab_clean = replace_nan_with_zero(f_state_date_currency_descr_tab)

    # вывод результата
    print(f"Всего банковских операций в выборке {len(f_state_date_currency_descr_tab_clean)}\n")
    print(format_transactions(f_state_date_currency_descr_tab_clean))


# ---------------------------------------------------------------------------------------------------------------------


# -----------------------------------------main tests------------------------------------------------------------------
if __name__ == "__main__":
    main()
