import pytest
from src.masks import get_mask_card_number, get_mask_acount

@pytest.mark.parametrize("str, exp_str", [
    ("1111222233334444", "1111 22** **** 4444"),
    ("4444333322221111", "4444 33** **** 1111"),
    ("1234567890123456", "1234 56** **** 3456")
])
def test_get_mask_card_number(str, exp_str):
    assert get_mask_card_number(str) == exp_str


@pytest.mark.parametrize("str, exp_str", [
    ("1111222233334444", "**4444"),
    ("4444333322221111", "**1111"),
    ("1234567890123456", "**3456"),
    ("12345", "**2345"),
    ("12345678900987654321","**4321")
])
def test_get_mask_acount(str, exp_str):
    assert get_mask_acount(str) == exp_str