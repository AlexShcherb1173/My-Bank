import json
import os

def read_json_file(filepath):
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
       Если файл пустой, содержит не список или не найден, функция возвращает пустой список. """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        return []

