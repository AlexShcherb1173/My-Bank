import masks


def mask_account_card(card_account_number: str) -> str:
    """Функция принимает строку с названием и номером карты или счета и возвращает строку соответсвующей
    маски номера карты или счета"""
    card_account_num = card_account_number.lower()
    substring = card_account_num[:4]
    if substring == "счет":
        card_acc_num_mask = masks.get_mask_acount(card_account_num[5:])
    else:
        account_num = ""
        for symbol in card_account_num:
            if symbol.isdigit():
                account_num += symbol
        card_acc_num_mask = masks.get_mask_card_number(account_num)
    return card_acc_num_mask


def get_date(date_time_in: str) -> str:
    """Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг"""
    date_form = ""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form
