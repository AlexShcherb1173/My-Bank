import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Возвращает список словарей, где поле 'description' содержит искомую строку (поиск нечувствителен к регистру)."""
    pattern = re.compile(rf"\b{re.escape(search)}\b", re.IGNORECASE)
    return [entry for entry in data if pattern.search(entry.get("description", ""))]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям (описаниям), входящим в список categories.
    Возвращает словарь вида {"Категория": количество}"""
    counter: Counter[str] = Counter()
    for tx in data:
        desc = tx.get("description", "").strip()
        if desc in categories:
            counter[desc] += 1
    return dict(counter)
