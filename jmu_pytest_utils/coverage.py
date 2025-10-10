"""Run test coverage and analyze the results."""

import importlib
import json
import os
import pytest
import random
import sys
import textwrap
import types

from collections.abc import Callable
from jmu_pytest_utils.common import run_command

TestFunction = Callable[..., None]


def _return_random(*args, **kwargs):
    """Function stub to replace the actual functions being tested."""
    return random.random()


def inject_random(main_filename: str) -> None:
    """Replace all functions in the given module with return_random.

    Args:
        main_filename: Name of the main file to test.
    """
    sys.path.insert(0, os.getcwd())  # for importlib
    module_name = main_filename[:-3].replace(os.path.sep, ".")
    module = importlib.import_module(module_name)
    for name, obj in vars(module).items():
        if isinstance(obj, types.FunctionType):
            obj.__code__ = _return_random.__code__


def _process_results_json(function: TestFunction, status: str, penalty: float) -> None:
    """Verify correctness in the results.json file.

    Args:
        function: Test function for score/weight.
        status: Check for "fail" or "pass" in status.
        penalty: Points per incorrect test function.
    """
    if not os.path.exists("results.json"):
        pytest.fail("pytest failed to generate test results", False)
    with open("results.json") as file:
        results = json.load(file)
    os.remove("results.json")

    # Count how many test functions didn't pass/fail correctly
    points = 0
    if status == "fail":
        output = "random return values\n"
    else:
        output = "actual return values\n"
    for test in results["tests"]:
        if test["status"] != status + "ed":  # failed / passed
            points += penalty
            output += f"* {test['name']} did not {status}\n"
            test_output = test.get("output")
            if test_output:
                output += textwrap.indent(test_output, "    ")
                output += "\n"

    # If the test didn't pass, set the score and show output
    if points:
        weight = getattr(function, "weight", 0)
        if weight:
            setattr(function, "score", max(weight - points, 0))
        pytest.fail(output)


def assert_fail(function: TestFunction, main_filename: str, test_filename: str,
                penalty: float = 1) -> None:
    """Run pytest and assert that all tests fail.

    Note: The --jmu option of the jmu_pytest_utils plugin
    patches all functions in main_filename to return random.

    Args:
        function: Test function for score/weight.
        main_filename: Name of the main file to test.
        test_filename: Name of the test file to run.
        penalty: Points per incorrect test function.
    """
    run_command([
        "pytest",
        "--jmu=" + main_filename,
        test_filename
    ])
    _process_results_json(function, "fail", penalty)


def assert_pass(function: TestFunction, main_filename: str, test_filename: str,
                penalty: float = 1) -> None:
    """Run pytest and assert that all tests pass.

    Args:
        function: Test function for score/weight.
        main_filename: Name of the main file to test.
        test_filename: Name of the test file to run.
        penalty: Points per incorrect test function.
    """
    run_command([
        "pytest",
        "--jmu=assert_pass",
        test_filename
    ])
    _process_results_json(function, "pass", penalty)


def assert_cover(function: TestFunction, main_filename: str, test_filename: str,
                 branches: bool = False, line_penalty: float = 1, branch_penalty: float = 1) -> None:
    """Run pytest and analyze coverage results.

    Args:
        function: Test function for score/weight.
        main_filename: Name of the main file to test.
        test_filename: Name of the test file to run.
        branches: Whether to report branch coverage.
        line_penalty: Points per missed line.
        branch_penalty: Points per missed branch.
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
    points = 0
    output = "incomplete coverage\n"
    functions = coverage["files"][main_filename]["functions"]
    for name, data in functions.items():
        missing_lines = data.get("missing_lines", [])
        missing_branches = data.get("missing_branches", [])

        # Generate output of which lines/branches were missed
        if missing_lines or missing_branches:
            output += f"* {name}\n"
            if missing_lines:
                points += len(missing_lines) * line_penalty
                output += "    Lines: "
                output += str(missing_lines)[1:-1]
                output += "\n"
            if missing_branches:
                points += len(missing_branches) * branch_penalty
                output += "    Branches: "
                output += str(missing_branches)[1:-1]
                output += "\n"

    # If the test didn't pass, set the score and show output
    if points:
        weight = getattr(function, "weight", 0)
        if weight:
            setattr(function, "score", max(weight - points, 0))
        pytest.fail(output)
