# Limited feedback is shown to students during the quiz. Before grading, the
# instructor clicks "Regrade All Submissions" to show the complete results.

import quiz3
from jmu_pytest_utils.meta import submission_closed
from jmu_pytest_utils.quiz import check_docstring, check_return_types


def sum_positive(numbers):
    # Wrapper to avoid "from import" errors.
    return quiz3.sum_positive(numbers)


def first_upper(text):
    # Wrapper to avoid "from import" errors.
    return quiz3.first_upper(text)


def test_docs():
    check_docstring(quiz3)


def test_types(tmp_path):
    check_return_types(
        (int, sum_positive, ([1, -2, 3, -4, 5],)),
        (str, first_upper, ("hello World",)),
    )


if submission_closed():

    def test_sum_positive():
        """sum_positive: typical cases"""
        assert sum_positive([1, -2, 3, -4, 5]) == 9
        assert sum_positive([-1, -2, -3]) == 0
        assert sum_positive([0, 0, 0]) == 0
        assert sum_positive([10, 20, 30]) == 60

    def test_sum_positive_edge():
        """sum_positive: edge cases"""
        assert sum_positive([]) == 0
        assert sum_positive([-5, 5]) == 5
        assert sum_positive([-1, 2, -3, 4]) == 6

    def test_first_upper():
        """first_upper: typical cases"""
        assert first_upper("helloWorld") == "W"
        assert first_upper("Python") == "P"
        assert first_upper("aBcDe") == "B"

    def test_first_upper_lower():
        """first_upper: all lowercase"""
        assert first_upper("python") is None
        assert first_upper("") is None

    def test_first_upper_edge():
        """first_upper: edge cases"""
        # Edge cases
        assert first_upper("123ABC") == "A"
        assert first_upper("!@#") is None
