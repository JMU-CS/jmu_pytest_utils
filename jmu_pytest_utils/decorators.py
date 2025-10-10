"""Decorators for test functions."""

from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def required() -> Callable[[F], F]:
    """Decorator for requiring a test to pass.

    If a required test fails, the remaining tests are hidden.

    Returns:
        The original function with required attribute set.
    """
    def wrapper(f: F) -> F:
        f.required = True
        return f
    return wrapper


def weight(value: int) -> Callable[[F], F]:
    """Decorator for setting a test's max_score.

    Args:
        value: The number of points the test is worth.

    Returns:
        The original function with weight attribute set.
    """
    def wrapper(f: F) -> F:
        f.weight = value
        return f
    return wrapper
