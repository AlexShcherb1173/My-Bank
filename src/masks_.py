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


def get_mask_acount(acount_num_in: str) -> str:
    """Функция принимает строку с цифрами номера счета и вовращает строку маску номера счета
    последние 4 цифры и две * перед ними"""
    acount_num_mask = "**"
    acount_num_mask += acount_num_in[-4:]
    return acount_num_mask
