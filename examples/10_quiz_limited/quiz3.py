"""Quiz 3.

Name: Some Student
"""


def sum_positive(numbers):
    """Return the sum of all positive numbers in a list.

    Args:
        numbers (list): Zero or more integers.

    Returns:
        int: Sum of the positive numbers.

    Example:
    >>> sum_positive([1, -2, 3, -4, 5])
    9
    >>> sum_positive([-1, -2, -3])
    0
    """
    total = 0
    for n in numbers:
        if n > 0:
            total += n
    return total


def first_upper(text):
    """Return the first uppercase letter in a string.

    Args:
        text (str): The string to search.

    Returns:
        str or None: First uppercase letter, or None.

    Example:
    >>> first_upper("hello World")
    'W'
    >>> first_upper("python")
    """
    for c in text:
        if c.isupper():
            return c
    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
