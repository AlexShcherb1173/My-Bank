import pytest


@pytest.fixture
def list_dict1():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594236727, "state": "CANCELED", "date": "2019-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict2():
    return [
        {"id": 41428829, "state": "EXECUTED", "": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "": "2018-09-12T21:27:25.241689"},
        {"id": 594236727, "state": "CANCELED", "": "2019-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict3():
    return [
        {"id": 41428829, "state": "", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict4():
    return [
        {"id": "", "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": "", "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict5():
    return [
        {"id": 41428829, "": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict6():
    return [
        {"": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def list_dict7():
    return [
        {"": 41428829, "state": "EXECUTED", "date": ""},
        {"": 939719570, "state": "EXECUTED", "date": ""},
        {"": 594226727, "state": "CANCELED", "date": ""},
        {"": 615064591, "state": "CANCELED", "date": ""},
    ]
