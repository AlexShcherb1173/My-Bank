import csv
import pandas as pd


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
