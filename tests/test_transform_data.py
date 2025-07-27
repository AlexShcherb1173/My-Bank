# Модуль Transform_Data
# Модуль выполняет различные преобразования данных транзакций

import math
from reformat_rec import *
from typing import Any, Dict, List

#-----------------------------transform_csv-----------------------------------------------------------------------
def transform_csv(input_dict: dict) -> dict:
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

#------------------------------transform_json-----------------------------------------------------------------------
def transform_json(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """функция, которая преобразует список словарей из формата json файла в формат, совместимый с
    csv и xlsx файлами. С проверкой наличия необходимых ключей и отбросыванием некорректных записей"""
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

#-------------------------replace_nan_with_zero--------------------------------------------------------------------
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

#-----------------------------format_transactions--------------------------------------------------------------------
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
#------------------