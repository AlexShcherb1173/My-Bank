from typing import Any
from src_old.masks_ import *


def mask_account_card(card_account_number: str) -> Any:
    """Функция принимает строку с названием и номером карты или счета и возвращает строку соответсnвующей
    маски номера карты или счета"""
    substring = card_account_number[:4]
    substring = substring.lower()
    if substring == "счет":
        card_acc_num_mask = "Счет " + get_mask_acount(card_account_number[5:])
    else:
        account_num = ""
        prefics = ""
        for symbol in card_account_number:
            if symbol.isdigit():
                account_num += symbol
            elif symbol.isalpha():
                prefics += symbol
            elif symbol == " ":
                prefics += symbol
            card_acc_num_mask = prefics + get_mask_card_number(account_num)
    return card_acc_num_mask


def get_date(date_time_in: str) -> str:
    """Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг"""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form
