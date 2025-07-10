import pytest
import generators
# def card_number_generator(start: str = '1', stop: str = '9999999999999999') -> str:
#
#     for num in range(int(start), int(stop)+1):
#         yield '{:04d} {:04d} {:04d} {:04d}'.format(num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4)

@pytest.mark.parametrize(
    "start, stop, exp_str",
    [
        ('1', '1', '0000 0000 0000 0001'),
        ('1111111111111111', '1111111111111111', '1111 1111 1111 1111'),
        ('9999999999999999', '9999999999999999', '9999 9999 9999 9999'),
        ('1111222233334444', '1111222233334444', '1111 2222 3333 4444'),
        ('123456789012345', '123456789012345', '0123 4567 8901 2345'),
    ],
)


def test_card_number_generator(start, stop, exp_str):
    assert list(generators.card_number_generator(start, stop))[0] == exp_str