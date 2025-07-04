from src.masks_ import get_mask_card_number
from src.masks_ import get_mask_acount

def mask_account_card(card_account_number: str) -> str:
    """Функция принимает строку с названием и номером карты или счета и возвращает строку соответсnвующей
    маски номера карты или счета"""
    card_account_num = card_account_number.lower()
    substring = card_account_num[:4]
    if substring == "счет":
        card_acc_num_mask = "Счет " + masks_.get_mask_acount(card_account_num[5:])
    else:
        account_num = ""
        prefics = ""
        for symbol in card_account_num:
            if symbol.isdigit():
                account_num += symbol
            elif symbol.isalpha():
                prefics += symbol
            elif symbol == " ":
                prefics += symbol

        prefics_title = prefics.title()
        card_acc_num_mask = prefics_title + " " + masks_.get_mask_card_number(account_num)
    return card_acc_num_mask


def get_date(date_time_in: str) -> str:
    """Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг"""
    date_form = ""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form
