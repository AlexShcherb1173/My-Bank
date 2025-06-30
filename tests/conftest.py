import pytest

@pytest.fixture
def list_dict():
    return [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

#@pytest.fixture
#def num_card():
#   return 1111222233334444
@pytest.mark.parametrise()

@pytest.fixture
def nub_acct():
    return 1234567890

@pytest.fixture
def num_card_acc():
    return

@pytest.fixture
def str_date():
    return