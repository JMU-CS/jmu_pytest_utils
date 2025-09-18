from jmu_pytest_utils.audit import assert_no_while, count_comments, count_regex_matches
from jmu_pytest_utils.common import assert_pep8, assert_docs, chdir_test
from jmu_pytest_utils.decorators import weight
import os
import pytest

from analyze import count_iris, filter_adult

FILENAME = "analyze.py"

# Putting this line at the module level allows running individual tests.
chdir_test()


@weight(2)
def test_pep8_docs():
    """PEP 8 and docstrings"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)


@weight(2)
def test_approach():
    assert_no_while(FILENAME)
    assert count_comments(FILENAME) > 2
    assert count_regex_matches(FILENAME, r"\bwith\b") == 2


@weight(3)
def test_count_flowers():
    assert count_iris("data/iris.csv") == {"setosa": 50, "versicolor": 50, "virginica": 50}
    assert count_iris("data/iris2.csv") == {"setosa": 45, "versicolor": 40, "virginica": 35}


def helper(name):
    src = f"data/{name}.csv"
    dst = f"data/{name}.out"
    exp = f"data/{name}.exp"
    # Call the function and check the result file
    filter_adult(src, dst)
    if not os.path.exists(dst):
        pytest.fail("output file was not created")
    # Compare the file contents with expected file
    with open(dst) as file1, open(exp) as file2:
        obtained = file1.read()
        expected = file2.read()
    # Delete the output file before passing/failing
    os.remove(dst)
    assert obtained == expected


@weight(3)
def test_filter_adult():
    helper("adult1")
    helper("adult2")
