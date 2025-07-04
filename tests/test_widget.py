import pytest
import masks_
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


@pytest.mark.parametrize("str, exp_str", [
    ("Maestro1596837868705199", "Maestro 1596 83** **** 5199"),
    ("Счет 64686473678894779589", "Счет **9589"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет35383033474447895560", "Счет **5560"),
    ("VisaClassic6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Platinum8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ("VisaGold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("счет  73654108430135874305", "Счет **4305"),
])
def test_mask_account_card(str, exp_str):
    assert mask_account_card(str) == exp_str

@pytest.mark.parametrize("str, exp_str", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2025-06-30T02:", "30.06.2025"),
    ("2025-07-01", "01.07.2025"),
    ("2021-01-01rkuryflfkhfglf", "01.01.2021"),
])
def test_get_date(str, exp_str):
    assert get_date(str) == exp_str

 #   Maestro1596837868705199
 #   Счет 64686473678894779589
 #   MasterCard 7158300734726758
 #   Счет35383033474447895560
 #   VisaClassic6831982476737658
 #    Visa Platinum8990922113665229
 #    VisaGold 5999414228426353
 #    Счет  73654108430135874305
