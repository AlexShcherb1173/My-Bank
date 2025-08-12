import re
from typing import List, Dict
from collections import Counter


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """ Возвращает список словарей, где поле 'description' содержит искомую строку (поиск нечувствителен к регистру)."""
    pattern = re.compile(rf'\b{re.escape(search)}\b', re.IGNORECASE)
    return [entry for entry in data if pattern.search(entry.get("description", ""))]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций для заданных категорий на основе 'description' (поиск по подстроке)"""
    result = {category: 0 for category in categories}

    for entry in data:
        description = entry.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1

    return result