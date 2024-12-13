from jmu_pytest_utils.common import assert_pep8, assert_docs, run_module
from jmu_pytest_utils.decorators import required, weight
from importlib import reload
from pytest import approx

import grader
import sphere
FILENAME = "sphere.py"
SUBMISSION_FILES = [FILENAME]  # grader.py not submitted


@required()
def test_module():
    """Check output and variables"""
    stdout = run_module(FILENAME)
    assert stdout == "", "program should have no output"
    # Make sure required variables exist
    assert sphere.surface_area
    assert sphere.volume


@weight(1)
def test_pep8_docs():
    """PEP 8 and docstring"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)


@weight(3)
def test_unit_circle():
    """Values when radius is 1"""
    grader.radius = 1
    reload(sphere)
    assert sphere.surface_area == approx(12.56637), "incorrect surface_area"
    assert sphere.volume == approx(4.18879), "incorrect volume"


@weight(3)
def test_other_int():
    """Values when radius is 7"""
    grader.radius = 7
    reload(sphere)
    assert sphere.surface_area == approx(615.75216), "incorrect surface_area"
    assert sphere.volume == approx(1436.75504), "incorrect volume"


@weight(3)
def test_other_float():
    """Values when radius is 1.618"""
    grader.radius = 1.618
    reload(sphere)
    assert sphere.surface_area == approx(32.89780), "incorrect surface_area"
    assert sphere.volume == approx(17.74288), "incorrect volume"
