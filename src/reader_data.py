# Модуль Reader_Data
# Модуль для считывания данных транзакций из файлов различных форматов

import csv
import json
import os
import sys

import pandas as pd

sys.path.append(os.path.abspath("src"))
from transform_data import transform_csv


# --------------------------read_transactions_from_csv--------------------------------------------------------------
def read_transactions_from_csv(file_path: str) -> list[dict]:
    """функция для считывания финансовых операций из CSV.
    Принимает путь к файлу CSV в качестве аргумента.
    Выдает список словарей с транзакциями."""
    transactions = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transaction = transform_csv(row)
            transactions.append(transaction)
    return transactions


# -----------------------------read_transactions_from_excel-----------------------------------------------------------
def read_transactions_from_excel(file_path: str) -> list[dict]:
    """Функция для считывания финансовых операций из Excel.
    Принимает путь к файлу Excel в качестве аргумента.
    Выдает список словарей с транзакциями."""
    df = pd.read_excel(file_path)
    transactions = df.to_dict(orient="records")
    return transactions


# ----------------------------read_json_file--------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------------------------------------------------
