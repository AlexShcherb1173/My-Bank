from src_old.processing import *


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


def test_filter_by_state(list_dict6):
    assert filter_by_state(list_dict6, "CANCELED") == [
        {"": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state(list_dict1):
    assert filter_by_state(list_dict1, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594236727, "state": "CANCELED", "date": "2019-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state(list_dict3):
    assert filter_by_state(list_dict3, "CANCELED") == [
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]


def test_filter_by_state(list_dict4):
    assert filter_by_state(list_dict4, "CANCELED") == [
        {"id": "", "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_sort_by_date(list_dict1):
    assert sort_by_date(list_dict1) == [
        {"id": 594236727, "state": "CANCELED", "date": "2019-09-12T21:27:25.241689"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date(list_dict1):
    assert sort_by_date(list_dict1, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594236727, "state": "CANCELED", "date": "2019-09-12T21:27:25.241689"},
    ]


def test_sort_by_date(list_dict4):
    assert sort_by_date(list_dict4) == [
        {"id": "", "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": "", "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date(list_dict5):
    assert sort_by_date(list_dict5, False) == [
        {"id": 939719570, "": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date(list_dict7):
    assert sort_by_date(list_dict7) == [
        {"": 41428829, "state": "EXECUTED", "date": ""},
        {"": 939719570, "state": "EXECUTED", "date": ""},
        {"": 594226727, "state": "CANCELED", "date": ""},
        {"": 615064591, "state": "CANCELED", "date": ""},
    ]
