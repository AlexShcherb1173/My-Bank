from dotenv import load_dotenv
from typing import Any
import os
import requests

load_dotenv()

API_URL = os.getenv("CURRENCY_API_URL")
API_KEY = os.getenv("CURRENCY_API_KEY")


def get_transaction_amount_rub(transaction: dict) -> Any:
    """Возвращает сумму транзакции в рублях.
    transaction: словарь с данными о транзакции
    return: сумма в рублях (float)
    """
    amount_str = transaction.get("operationAmount", {}).get("amount", "0")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("tests", "RUB")

    try:
        amount = float(amount_str)
    except ValueError:
        return 0.0

    if currency_code == "RUB":
        return round(amount, 2)

    if currency_code not in ("USD", "EUR"):
        return 0.0

    try:
        response = requests.get(API_URL, params={"base": currency_code, "symbols": "RUB"}, headers={"apikey": API_KEY})
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return 0.0
