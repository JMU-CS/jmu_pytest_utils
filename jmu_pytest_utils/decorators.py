"""Test function decorators."""


def required():
    """Decorator for requiring a test to pass.

    If a required test fails, the remaining tests are hidden.

    Returns:
        function: The original function with attribute set.
    """
    def wrapper(f):
        f.required = True
        return f
    return wrapper


def weight(value):
    """Decorator for setting a test's max_score.

    Args:
        value (int): The number of points the test is worth.

    Returns:
        function: The original function with attribute set.
    """
    def wrapper(f):
        f.weight = value
        return f
    return wrapper
