"""Functions for working with triangles.

A triangle is represented by a tuple (a, b, c),
which defines the length of the three sides.
"""

import math


def valid(tri):
    """Check if a tuple represents a valid triangle.

    Args:
        tri (tuple): length of the three sides

    Returns:
        bool: True if valid, False otherwise
    """
    # if not exactly three sides
    if len(tri) != 3:
        return False
    a, b, c = sorted(tri)
    # if any side is not positive
    if a <= 0:
        return False
    # longest side is not too long
    return c < a + b


def area(tri):
    """Calculate the area using Heron's Formula.

    Args:
        tri (tuple): length of the three sides

    Raises:
        ValueError: if the triangle is invalid

    Returns:
        float: area of the triangle
    """
    if not valid(tri):
        raise ValueError("invalid triangle")
    # calculate half the perimeter
    a, b, c = tri
    s = 0.5 * (a + b + c)
    # calculate the triangle area
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def classify(tri):
    """Determine the type of triangle.

    Args:
        tri (tuple): length of the three sides

    Raises:
        ValueError: if the triangle is invalid

    Returns:
        str: "Equilateral", "Isosceles", or "Scalene"
    """
    if not valid(tri):
        raise ValueError("invalid triangle")
    a, b, c = tri
    if a == b == c:
        return "Equilateral"
    elif a == b or b == c or a == c:
        return "Isosceles"
    else:
        return "Scalene"
