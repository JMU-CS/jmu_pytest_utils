"""Analyze coverage for test_triangles."""

from jmu_pytest_utils.common import assert_pep8
from jmu_pytest_utils.coverage import assert_fail, assert_pass, assert_cover
from jmu_pytest_utils.decorators import required, weight

SUBMISSION_FILES = ["test_triangles.py"]
ADDITIONAL_FILES = ["triangles.py"]


@weight(1)
def test_pep8():
    assert_pep8("test_triangles.py")


@required()
@weight(2)
def test_fail():
    """All tests should fail when given random return values"""
    assert_fail(test_fail, "triangles.py", "test_triangles.py")


@required()
@weight(2)
def test_pass():
    """All tests should pass when given actual return values"""
    assert_pass(test_pass, "triangles.py", "test_triangles.py")


@weight(5)
def test_cover():
    """Code coverage: all statements should run during tests"""
    assert_cover(test_cover, "triangles.py", "test_triangles.py")
