import csv
import os
import logging
import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
file_handler = logging.FileHandler(r'logs\reader.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def read_transactions_from_csv(filepath: str) -> list:
    """ функция для считывания финансовых операций из CSV.
        Принимает путь к файлу CSV в качестве аргумента.
        Выдает список словарей с транзакциями."""
    if not os.path.exists(filepath):
        logger.error(f"Файл CSV не найден: {filepath}")
        return []

    try:
        with open(filepath,  mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            transactions = list(reader)
            logger.debug(f"Файл CSV успешно прочитан: {filepath}, записей: {len(transactions)}")
            return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        return []


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
file_handler = logging.FileHandler(r'logs\reader.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def read_transactions_from_excel(filepath: str) -> list:
    """функция для считывания финансовых операций из Excel.
        Принимает путь к файлу Excel в качестве аргумента.
        Выдает список словарей с транзакциями."""
    if not os.path.exists(filepath):
        logger.error(f"Файл Excel не найден: {filepath}")
        return []

    try:
        df = pd.read_excel(filepath)
        transactions = df.to_dict(orient='records')
        logger.debug(f"Файл Excel успешно прочитан: {filepath}, записей: {len(transactions)}")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel: {e}")
        return []