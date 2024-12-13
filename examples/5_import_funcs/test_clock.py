from jmu_pytest_utils.common import assert_pep8, assert_docs
from jmu_pytest_utils.decorators import weight

from clock import time_str, add_time
FILENAME = "clock.py"


@weight(2)
def test_pep8_docs():
    """PEP 8 and docstrings"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)


@weight(2)
def test_time_str_easy():
    """time_str() easy cases"""
    assert time_str(10, 15) == "10:15 AM", "time_str(10, 15)"
    assert time_str(23, 30) == "11:30 PM", "time_str(23, 30)"


@weight(2)
def test_time_str_hard():
    """time_str() hard cases"""
    assert time_str(0, 0) == "12:00 AM", "time_str(0, 0)"
    assert time_str(17, 5) == "05:05 PM", "time_str(17, 5)"


@weight(2)
def test_add_time_easy():
    """add_time() easy cases"""
    assert add_time(10, 0, 45) == "10:45 AM", "45 minutes after 10:00 AM"
    assert add_time(22, 45, -15) == "10:30 PM", "15 minutes before 10:30 PM"


@weight(2)
def test_add_time_hard():
    """add_time() hard cases"""
    assert add_time(0, 0, 5*24*60) == "12:00 AM", "5 days after midnight"
    assert add_time(1, 15, 2*24*60 + 75) == "02:30 AM", "2 days and 75 minutes after 01:15 AM"
