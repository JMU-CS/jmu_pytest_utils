"""Run test coverage and analyze the results."""

import importlib
import os
import pytest
import sys
import types

from jmu_pytest_utils.common import run_command


def return_random(*args, **kwargs):
    """Function stub to replace the actual functions being tested."""
    import random
    return random.random()


def inject_random(main_filename):
    """Replace all functions in the given module with return_random.

    Args:
        main_filename (str): Name of the main file to test.
    """
    sys.path.insert(0, os.getcwd())  # for importlib
    module_name = main_filename[:-3].replace(os.path.sep, ".")
    module = importlib.import_module(module_name)
    for name, obj in vars(module).items():
        if isinstance(obj, types.FunctionType):
            obj.__code__ = return_random.__code__


def assert_fail(main_filename, test_filename):
    """Run pytest and assert that all tests fail.

    This test patches all functions to return random numbers.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.
    """
    run_command([
        "pytest",
        "--jmu=" + main_filename,
        test_filename
    ])
    if not os.path.exists("results.json"):
        pytest.fail("pytest failed to generate test results", False)
    pass  # TODO
    os.remove("results.json")


def assert_pass(main_filename, test_filename):
    """Run pytest and assert that all tests pass.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.
    """
    run_command([
        "pytest",
        "--jmu=assert_pass",
        test_filename
    ])
    if not os.path.exists("results.json"):
        pytest.fail("pytest failed to generate test results", False)
    pass  # TODO
    os.remove("results.json")


def assert_cover(main_filename, test_filename):
    """Run pytest and analyze coverage results.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.
    """
    run_command([
        "pytest",
        "--cov=" + main_filename[:-3],  # remove .py suffix
        "--cov-branch",
        "--cov-report=json",
        test_filename
    ])
    if not os.path.exists("coverage.json"):
        pytest.fail("pytest failed to generate coverage results", False)
    pass  # TODO
    os.remove("coverage.json")
