# Модуль Reformat_rec
# Модуль выполняет преобразования отдельных полей записей в структуре данных

from typing import Any


# ---------------------get_mask_card_numbe---------------------------------------------------------------------------
def get_mask_card_number(card_num_in: str) -> str:
    """Функция принимает строку с 16 цифрами номера карты и вовращает строку маску номера карты
    по 4 цифры через пробел, с 6й по 12ю цифру замена на *"""
    card_num_mask = ""
    for i in range(len(card_num_in)):
        if i > 5 and i < 12:
            card_num_mask += "*"
        else:
            card_num_mask += card_num_in[i]
    substring_1 = card_num_mask[:4]
    substring_2 = card_num_mask[4:8]
    substring_3 = card_num_mask[8:12]
    substring_4 = card_num_mask[12:16]
    card_num_mask = substring_1 + " " + substring_2 + " " + substring_3 + " " + substring_4
    return card_num_mask


# ----------------------get_mask_acount-----------------------------------------------------------------------------
def get_mask_acount(acount_num_in: str) -> str:
    """Функция принимает строку с цифрами номера счета и вовращает строку маску номера счета
    последние 4 цифры и две * перед ними"""
    acount_num_mask = "**"
    acount_num_mask += acount_num_in[-4:]
    return acount_num_mask


# ------------------------------------mask_account_card-------------------------------------------------------------
def mask_account_card(card_account_number: str) -> Any:
    """Функция принимает строку с названием и номером карты или счета и возвращает строку соответсnвующей
    маски номера карты или счета"""
    substring = card_account_number[:4]
    substring = substring.lower()
    card_acc_num_mask = ""
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
    # print(card_acc_num_mask)
    return card_acc_num_mask


# ---------------------get_date---------------------------------------------------------------------------------------
def get_date(date_time_in: str) -> str:
    """Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг"""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form


# ---------------------------------------------------------------------------------------------------------------------
