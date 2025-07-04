import pytest

def filter_by_state(list_dict: list, state_in="EXECUTED") -> list:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
       словарей-выборку по полю state"""
    list_dict_filter_state = []
    for i in list_dict:
        if i["state"] == state_in:
            list_dict_filter_state.append(i)

    return list_dict_filter_state


def sort_by_date(list_dict: list, reverse=True) -> list:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
       словарей сортированных по date(назад или вперед)"""
    if reverse:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id:id["date"], reverse=True)
    else:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=False)
    return list_dict_sort_by_date



def test_filter_by_state(list_dict1):
    assert filter_by_state(list_dict1) == [
        {'': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}

             ]

def test_filter_by_state(list_dict2):
    assert filter_by_state(list_dict2) == [
        {'': 41428829, 'state': 'EXECUTED', '': '2019-07-03T18:35:29.512364'},
        {'': 939719570, 'state': 'EXECUTED', '': '2018-06-30T02:08:58.425572'}

        ]

def test_filter_by_state(list_dict3):
    assert filter_by_state(list_dict3) == [
            {'': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}

            ]

def test_filter_by_state(list_dict4):
    assert filter_by_state(list_dict4) == [
        {'id': null, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}

        ]

def test_filter_by_state(list_dict5):
    assert filter_by_state(list_dict5) == [
        {'id': 41428829, '': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, '': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]

def test_filter_by_state(list_dict6):
    assert filter_by_state(list_dict6) == [
        {'': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]

def test_sort_by_date(list_dict1):
    assert sort_by_date(list_dict1) == [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
            ]

