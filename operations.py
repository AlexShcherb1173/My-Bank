import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Возвращает список словарей, где поле 'description' содержит искомую строку (поиск нечувствителен к регистру).

    :param data: список словарей с банковскими операциями
    :param search: строка поиска
    :return: список словарей, соответствующих критерию поиска
    """
    pattern = re.compile(rf'\b{re.escape(search)}\b', re.IGNORECASE)
    return [entry for entry in data if pattern.search(entry.get("description", ""))]


from typing import List, Dict
from collections import Counter


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций для заданных категорий на основе поля 'description'.

    :param data: список словарей с банковскими операциями
    :param categories: список категорий (строк), которые нужно искать в description
    :return: словарь вида {категория: количество}
    """
    # Собираем все descriptions, которые есть в транзакциях
    descriptions = [entry.get("description", "") for entry in data]

    # Подсчитываем все описания
    counter = Counter(descriptions)

    # Возвращаем только те, которые есть в categories
    return {category: counter.get(category, 0) for category in categories}