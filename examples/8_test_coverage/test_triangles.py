"""Test the provided triangles module.

This file is submitted by the student.
"""

from pytest import approx, raises
from triangles import valid, area, classify


def test_valid():
    # NOTE: You should never type "== True".
    assert valid((3, 4, 5))
    # NOTE: You should never type "== False".
    assert not valid((3, 4, 10))
    assert not valid((3, 4, 10, 20))
    assert not valid((-3, 4, 10))


def test_area():
    # NOTE: Use approx() to avoid floating-point errors.
    assert area((3, 4, 5)) == approx(6.0)
    # NOTE: Use raises() to check if errors are raised.
    with raises(ValueError):
        area((3, 4, 10))


def test_classify():
    with raises(ValueError):
        classify((-3, 4, 10))
    assert classify((3, 3, 3)) == "Equilateral"
    assert classify((3, 3, 5)) == "Isosceles"
    assert classify((3, 4, 5)) == "Scalene"
