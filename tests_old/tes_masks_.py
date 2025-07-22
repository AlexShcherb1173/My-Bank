import pytest
from src_old.masks_ import get_mask_card_number
from src_old.masks_ import get_mask_acount


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
