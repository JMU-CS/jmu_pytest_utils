from jmu_pytest_utils.audit import count_calls
from jmu_pytest_utils.common import assert_pep8, assert_docs, run_module
from jmu_pytest_utils.decorators import required, weight

FILENAME = "welcome.py"

# Autograder settings (used to generate config.sh)
SUBMISSION_FILES = [FILENAME]
AUTOGRADER_TESTS = ["test_welcome.py"]
ADDITIONAL_FILES = []
SUBMISSION_LIMIT = 10
FUNCTION_TIMEOUT = 1
SCHOOL_TIME_ZONE = "US/Mountain"


@required()
def test_two_prints():
    """Two print statements"""
    assert count_calls(FILENAME, "print") == 2


@weight(2)
def test_pep8_docs():
    """PEP 8 and docstrings"""
    assert_pep8(FILENAME)
    assert_docs(FILENAME)


@weight(4)
def test_output_alan():
    """Input: Alan"""
    stdout = run_module(FILENAME, "Alan\n")
    assert stdout == "Welcome to Python 3!\nWhat's your name? Alan is a great name!\n"


@weight(4)
def test_output_grace():
    """Input: Grace"""
    stdout = run_module(FILENAME, "Grace\n")
    assert stdout == "Welcome to Python 3!\nWhat's your name? Grace is a great name!\n"
