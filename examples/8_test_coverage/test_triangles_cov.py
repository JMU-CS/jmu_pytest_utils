"""Analyze coverage for test_triangles."""

from jmu_pytest_utils.common import assert_pep8
from jmu_pytest_utils.coverage import assert_fail, assert_pass, assert_cover
from jmu_pytest_utils.decorators import required, weight
import pytest

SUBMISSION_FILES = ["test_triangles.py"]
ADDITIONAL_FILES = ["triangles.py"]


@weight(1)
def test_pep8():
    assert_pep8("test_triangles.py")


@required()
@weight(2)
def test_fail():
    """All tests should fail when given random return values"""
    count, output = assert_fail("triangles.py", "test_triangles.py")
    if count:
        test_fail.score = max(test_fail.weight - count, 0)
        pytest.fail(output)


@required()
@weight(2)
def test_pass():
    """All tests should pass when given actual return values"""
    count, output = assert_pass("triangles.py", "test_triangles.py")
    if count:
        test_pass.score = max(test_pass.weight - count, 0)
        pytest.fail(output)


@weight(5)
def test_cover():
    """Code coverage: all statements should run during tests"""
    count, output = assert_cover("triangles.py", "test_triangles.py", True)
    if count:
        test_cover.score = max(test_cover.weight - count, 0)
        pytest.fail(output)
