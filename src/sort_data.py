# Модуль Sort_Data
# Модуль выполняет сортировку массива данных по различным критериям

import re
from typing import Dict, List


# --------------------------process_bank_search------------------------------------------------------------------------
def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Возвращает список словарей, где поле 'description' содержит искомую строку (поиск нечувствителен к регистру)."""
    pattern = re.compile(rf"\b{re.escape(search)}\b", re.IGNORECASE)
    return [entry for entry in data if pattern.search(entry.get("description", ""))]


# --------------------------filter_and_sort_by_currency---------------------------------------------------------------
def filter_and_sort_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Принимает список транзакций и код валюты.
    Возвращает отсортированный список транзакций, в которых currency_code совпадает."""
    filtered = [tx for tx in transactions if tx.get("currency_code") == currency_code]
    sorted_filtered = sorted(filtered, key=lambda tx: tx["currency_code"])
    return sorted_filtered


# ---------------------------filter_by_state--------------------------------------------------------------------------
def filter_by_state(list_dict: list[dict], state_in: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей-выборку по полю state"""
    list_dict_filer_state = []
    for account in list_dict:
        # print(account)
        if account["state"] == state_in:
            list_dict_filer_state.append(account)
    return list_dict_filer_state


# ----------------------------sort_by_date----------------------------------------------------------------------
def sort_by_date(list_dict: list[dict], reverse: bool = True) -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей сортированных по date(назад или вперед)"""
    if reverse:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=True)
    else:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=False)
    return list_dict_sort_by_date


# -------------------------------------------------------------------------------------------------------------------
