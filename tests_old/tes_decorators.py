import os
import pytest
from src_old.decorators import *

LOG_FILE = "test_log.txt"

@log()
def add(a, b):
    return a + b

@log()
def fail_func(a, b):
    return a / b  # Возможна ZeroDivisionError

@log(filename=LOG_FILE)
def multiply(x, y):
    return x * y

@log(filename=LOG_FILE)
def crash(x):
    raise ValueError("something went wrong")

def test_add_console_log(capsys):
    result = add(3, 5)
    captured = capsys.readouterr()

    assert result == 8
    assert "add start" in captured.err
    assert "add ok" in captured.err


def test_fail_console_log(capsys):
    with pytest.raises(ZeroDivisionError):
        fail_func(10, 0)
    captured = capsys.readouterr()

    assert "fail_func start" in captured.err
    assert "fail_func error: ZeroDivisionError." in captured.err
    assert "Inputs: (10, 0), {}" in captured.err


def test_multiply_file_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    result = multiply(2, 4)
    assert result == 8

    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()
        assert "multiply start" in content
        assert "multiply ok" in content


def test_crash_file_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    with pytest.raises(ValueError):
        crash(123)

    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()
        assert "crash start" in content
        assert "crash error: ValueError." in content
        assert "Inputs: (123,), {}" in content
