from src.processing import *


def test_filter_by_state(list_dict2):
    assert filter_by_state(list_dict2) == [
        {"": 41428829, "state": "EXECUTED", "": "2019-07-03T18:35:29.512364"},
        {"": 939719570, "state": "EXECUTED", "": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state(list_dict3):
    assert filter_by_state(list_dict3) == [{"": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]


def test_filter_by_state(list_dict4):
    assert filter_by_state(list_dict4) == [
        {"id": null, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state(list_dict6):
    assert filter_by_state(list_dict6) == [
        {"": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

