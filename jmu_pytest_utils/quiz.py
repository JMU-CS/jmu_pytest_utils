"""Helper functions used during in-class quizzes."""

from types import ModuleType
from typing import Any, Callable

import pytest
from jmu_pytest_utils.coverage import get_caller


def check_docstring(module: ModuleType, min_len: int = 15) -> None:
    """Verify that a module's docstring exists.

    If the calling test function does not already have a docstring, the
    docstring is automatically set to "Check for docstring."

    If the check passes, the `output` attribute of the test function is
    set to report the docstring's length.

    Args:
        module: The module to examine.
        min_len: Minimum length of the docstring.
    """

    # Set the test function's docstring
    test_func = get_caller()
    if not test_func.__doc__:
        test_func.__doc__ = "Check for docstring"

    # Check for the module's docstring
    assert module.__doc__, "Missing module docstring"
    length = len(module.__doc__)
    assert length >= min_len, "❌ Docstring is too short"
    test_func.output = f"✅ Docstring is {length} characters"


def _type_name(value: Any) -> str:
    """Format the name of an object's type name for output.

    Args:
        value: The value returned from a function.

    Returns:
        str: A phrase like "None", "an int", or "a str".
    """
    name = type(value).__name__
    if name == "NoneType":
        return "None"
    elif name.startswith(("a", "e", "i", "o", "u")):
        return "an " + name
    else:
        return "a " + name


def check_return_types(
    *calls: tuple[type, Callable[..., Any], tuple[Any, ...]],
) -> None:
    """Verify the return type of one or more function calls.

    If the calling test function does not already have a docstring, the
    docstring is automatically set to "Check return types."

    This function builds a result string with a ✅ or ❌ for each call.
    If any return type is incorrect, pytest.fail() is called. Otherwise,
    the `output` attribute of the test function is set.

    Args:
        calls: Tuples of (expected_type, function, *args).
    """
    output = ""
    for expected_type, function, args in calls:
        try:
            result = function(*args)
            if isinstance(result, expected_type):
                output += f"✅ {function.__name__}() returned {_type_name(result)}\n"
            else:
                output += f"❌ {function.__name__}() returned {_type_name(result)}\n"
        except Exception as e:
            output += f"❌ {function.__name__}() raised {type(e).__name__}: {e}\n"

    # Set the test function's docstring
    test_func = get_caller()
    if not test_func.__doc__:
        test_func.__doc__ = "Check return types"

    # Set the test function's output
    if "❌" in output:
        pytest.fail("\n" + output)
    else:
        test_func.output = output
