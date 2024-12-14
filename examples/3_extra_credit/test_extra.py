from jmu_pytest_utils.common import assert_pep8, assert_docs
from jmu_pytest_utils.decorators import weight
import pytest

FILENAME = "extra.py"


def test_pep8_docs():
    """PEP 8 and docstring"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)
    # Manually assign the function's output and score
    test_pep8_docs.output = "Extra point for good style!"
    test_pep8_docs.score = 1


@weight(5)
def test_partial():
    # Setting the score takes precedence over weight
    test_partial.output = "Partial credit example"
    test_partial.score = 2


@weight(5)
def test_skip():
    pytest.skip("Points given unless test fails")
    assert 0 == 1
