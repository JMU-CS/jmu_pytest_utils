"""Analyze coverage for test_triangles."""

from jmu_pytest_utils.common import assert_pep8, run_pytest
from jmu_pytest_utils.decorators import required, weight

SUBMISSION_FILES = ["test_triangles.py"]
ADDITIONAL_FILES = ["triangles.py"]


def setup_module(module):
    run_pytest("triangles.py", "test_triangles.py")


@weight(1)
def test_pep8():
    assert_pep8("test_triangles.py")


@required()
@weight(2)
def test_stubs_fail():
    pass


@required()
@weight(2)
def test_solution_pass():
    pass


@weight(5)
def test_coverage():
    pass
