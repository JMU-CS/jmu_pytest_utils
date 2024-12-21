"""Run test coverage and analyze the results."""

import importlib
import json
import os
import pytest
import sys
import textwrap
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


def process_results_json(status):
    """Verify correctness in results.json file.

    Args:
        status (str): Check for "fail" or "pass" in status.

    Returns:
        int, str: Number of errors and corresponding output.
    """
    if not os.path.exists("results.json"):
        pytest.fail("pytest failed to generate test results", False)
    with open("results.json") as file:
        results = json.load(file)
    os.remove("results.json")

    # Count how many test functions didn't pass/fail correctly
    count = 0
    if status == "fail":
        output = "random return values\n"
    else:
        output = "actual return values\n"
    for test in results["tests"]:
        if test["status"] != status + "ed":  # failed / passed
            count += 1
            output += f"* {test['name']} did not {status}\n"
            test_output = test.get("output")
            if test_output:
                output += textwrap.indent(test_output, "    ")
                output += "\n"
    return count, output


def assert_fail(main_filename, test_filename):
    """Run pytest and assert that all tests fail.

    Note: The --jmu option of the jmu_pytest_utils plugin
    patches all functions in main_filename to return random.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.

    Returns:
        int, str: Number of errors and corresponding output.
    """
    run_command([
        "pytest",
        "--jmu=" + main_filename,
        test_filename
    ])
    return process_results_json("fail")


def assert_pass(main_filename, test_filename):
    """Run pytest and assert that all tests pass.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.

    Returns:
        int, str: Number of errors and corresponding output.
    """
    run_command([
        "pytest",
        "--jmu=assert_pass",
        test_filename
    ])
    return process_results_json("pass")


def assert_cover(main_filename, test_filename, branches=False):
    """Run pytest and analyze coverage results.

    Args:
        main_filename (str): Name of the main file to test.
        test_filename (str): Name of the test file to run.

    Returns:
        int, str: Number of missed and corresponding output.
    """
    run_command([
        "pytest",
        "--cov=" + main_filename[:-3],  # remove .py suffix
        "--cov-branch" if branches else "",
        "--cov-report=json",
        test_filename
    ])
    if not os.path.exists("coverage.json"):
        pytest.fail("pytest failed to generate coverage results", False)
    with open("coverage.json") as file:
        coverage = json.load(file)
    os.remove("coverage.json")

    # Count how many lines were missed in each function
    count = 0
    output = "incomplete coverage\n"
    functions = coverage["files"][main_filename]["functions"]
    for name, data in functions.items():
        missing_lines = data.get("missing_lines", [])
        missing_branches = data.get("missing_branches", [])
        missed = len(missing_lines) + len(missing_branches)
        if missed:
            count += missed
            output += f"* {name}\n"
            if missing_lines:
                output += "    Lines: "
                output += str(missing_lines)[1:-1]
                output += "\n"
            if missing_branches:
                output += "    Branches: "
                output += str(missing_branches)[1:-1]
                output += "\n"
    return count, output
