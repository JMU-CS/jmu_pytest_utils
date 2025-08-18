"""Common test functions used in many autograders."""

import inspect
import json
import os
import pytest
import subprocess


def chdir_test():
    """Change the current directory to that of the test module.

    This function ensures that tests run smoothly both offline
    (in VS Code) and on Gradescope.
    """
    for frame_info in inspect.stack()[1:]:
        basename = os.path.basename(frame_info.filename)
        if basename.startswith("test_"):
            dirname = os.path.dirname(frame_info.filename)
            os.chdir(dirname)
            break


def get_username(default="username"):
    """Get the student's username from the submission metadata.

    Args:
        default (str): Value to return if metadata not found.

    Returns:
        str: The student's email address up to the @ symbol.
    """
    try:
        with open("/autograder/submission_metadata.json") as file:
            metadata = json.load(file)
            return metadata["users"][0]["email"].split("@")[0]
    except FileNotFoundError:
        return default


def _get_cfg(filename):
    """Get the path of an optional configuration file.

    Args:
        filename: Config file (Ex: "flake8.cfg").

    Returns:
        str: Relative or absolute path to config file.
    """
    if os.path.exists(filename):
        return filename
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, "template", filename)


def assert_pep8(filename):
    """Run flake8 with flake8.cfg on the given file.

    Args:
        filename (str): The source file to check.
    """
    chdir_test()
    result = subprocess.run(["flake8", "--config=" + _get_cfg("flake8.cfg"), filename],
                            capture_output=True, text=True)
    if result.returncode:
        pytest.fail("PEP 8 issues:\n" + "\n".join("  " +
                    line for line in result.stdout.splitlines()), False)


def assert_docs(filename):
    """Run flake8 with docstring.cfg on the given file.

    Args:
        filename (str): The source file to check.
    """
    chdir_test()
    result = subprocess.run(["flake8", "--config=" + _get_cfg("docstring.cfg"), filename],
                            capture_output=True, text=True)
    if result.returncode:
        pytest.fail("Docstring issues:\n" + "\n".join("  " +
                    line for line in result.stdout.splitlines()), False)


def ruff_check(filename):
    """Run 'ruff check' with ruff.toml on the given file.

    Args:
        filename (str): The source file to check.
    """
    chdir_test()
    result = subprocess.run(["ruff", "check", filename, "--config", _get_cfg("ruff.toml")],
                            capture_output=True, text=True)
    if result.returncode:
        pytest.fail("\n".join("  " + line for line in result.stdout.splitlines()), False)


def run_command(args, input=None):
    """Run the given command in a subprocess.

    Args:
        args (list): The command (and args) to run.
        input (str): Standard input from the user.

    Returns:
        str: Captured output from the child process.
    """
    chdir_test()
    result = subprocess.run(args, input=input, capture_output=True, text=True)
    if result.stderr:
        # remove absolute paths from the traceback
        reason = result.stderr.replace(os.getcwd() + os.path.sep, "")
        pytest.fail(reason, False)
    return result.stdout


def run_module(filename, input=None):
    """Run the given module in a subprocess.

    Args:
        filename (str): The source file to run.
        input (str): Standard input from the user.

    Returns:
        str: Captured output from the child process.
    """
    return run_command(["python", filename], input)
