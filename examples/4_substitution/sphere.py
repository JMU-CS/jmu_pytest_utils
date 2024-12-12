"""Compute the surface area and volume of a sphere."""

from grader import radius
import math

# These variables will be checked by the autograder.
surface_area = 4 * math.pi * radius ** 2
volume = (4 / 3) * math.pi * radius ** 3
