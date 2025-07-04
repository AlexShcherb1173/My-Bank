import pytest
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
    card_num_mask = (
        substring_1 + " " + substring_2 + " " + substring_3 + " " + substring_4
    )
    return card_num_mask


def get_mask_acount(acount_num_in: str) -> str:
    """Функция принимает строку с цифрами номера счета и вовращает строку маску номера счета
         последние 4 цифры и две * перед ними"""
    acount_num_mask = "**"
    acount_num_mask += acount_num_in[-4:]
    return acount_num_mask

def mask_account_card(card_account_number: str) -> str:
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
    date_form = ""
    date_form = date_time_in[8:10] + "." + date_time_in[5:7] + "." + date_time_in[:4]
    return date_form


@pytest.mark.parametrize("str, exp_str", [
    ("Maestro1596837868705199", "Maestro1596 83** **** 5199"),
    ("Счет 64686473678894779589", "Счет **9589"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет35383033474447895560", "Счет **5560"),
    ("VisaClassic6831982476737658", "VisaClassic6831 98** **** 7658"),
    ("Visa Platinum8990922113665229", "Visa Platinum8990 92** **** 5229"),
    ("VisaGold 5999414228426353", "VisaGold 5999 41** **** 6353"),
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

