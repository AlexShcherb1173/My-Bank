from main import *
import pytest


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("Maestro1596837868705199", "Maestro1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет35383033474447895560", "Счет **5560"),
        ("VisaClassic6831982476737658", "VisaClassic6831 98** **** 7658"),
        ("Visa Platinum8990922113665229", "Visa Platinum8990 92** **** 5229"),
        ("VisaGold 5999414228426353", "VisaGold 5999 41** **** 6353"),
        ("счет  73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(str, exp_str):
    assert mask_account_card(str) == exp_str


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-06-30T02:", "30.06.2025"),
        ("2025-07-01", "01.07.2025"),
        ("2021-01-01rkuryflfkhfglf", "01.01.2021"),
    ],
)
def test_get_date(str, exp_str):
    assert get_date(str) == exp_str

@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("1111222233334444", "1111 22** **** 4444"),
        ("4444333322221111", "4444 33** **** 1111"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("11112222333344445", "1111 22** **** 4444"),
        ("111122223333444", "1111 22** **** 444"),
        ("111abc22333344sd", "111a bc** **** 44sd"),
        ("111abc2244sd", "111a bc** **** "),
        ("", "   "),
    ],
)
def test_get_mask_card_number(str, exp_str):
    assert get_mask_card_number(str) == exp_str


@pytest.mark.parametrize(
    "str, exp_str",
    [
        ("1111222233334444", "**4444"),
        ("4444333322221111", "**1111"),
        ("1234567890123456", "**3456"),
        ("12345", "**2345"),
        ("12345678900987654321", "**4321"),
        ("1234567890098765aaaa", "**aaaa"),
        ("", "**"),
    ],
)
def test_get_mask_acount(str, exp_str):
    assert get_mask_acount(str) == exp_str

