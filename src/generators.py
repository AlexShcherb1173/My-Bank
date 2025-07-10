# def filter_by_currency
#     pass
#
# def transaction_descriptions:
#     pass


def card_number_generator(start: str = '1', stop: str = '9999999999999999') -> str:

    for num in range(int(start), int(stop)+1):
        yield '{:04d} {:04d} {:04d} {:04d}'.format(num // 10**12, (num // 10**8) % 10**4, (num // 10**4) % 10**4, num % 10**4)


