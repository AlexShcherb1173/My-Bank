import json
import os
import logging

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# FileHandler
file_handler = logging.FileHandler("utils.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Formatter: время, модуль, уровень, сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json_file(filepath: str) -> list:
    """
    Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден — возвращает пустой список.
    """
    if not os.path.exists(filepath):
        logger.error(f"Файл не найден: {filepath}")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                logger.debug(f"Файл успешно прочитан: {filepath}, найдено записей: {len(data)}")
                return data
            else:
                logger.error(f"Некорректный формат данных в файле: {filepath}")
                return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {filepath}: {e}")
        return []
    except IOError as e:
        logger.error(f"I/O ошибка при чтении файла {filepath}: {e}")
        return []