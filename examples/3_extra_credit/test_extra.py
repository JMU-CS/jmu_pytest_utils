from jmu_pytest_utils.common import assert_pep8, assert_docs
from jmu_pytest_utils.decorators import weight
import pytest

FILENAME = "extra.py"


def test_pep8_docs():
    """PEP 8 and docstring"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)
    # Manually assign the function's output and score
    test_pep8_docs.output = "Extra credit for passing!"
    test_pep8_docs.score = 2


@weight(5)
def test_fail():
    pytest.fail("No way this will pass")


@weight(5)
def test_skip():
    pytest.skip("This test is silly")
    assert 0 == 1
