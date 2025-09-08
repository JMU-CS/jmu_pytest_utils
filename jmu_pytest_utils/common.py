"""Common test functions used in many autograders."""

from datetime import datetime, timedelta, timezone
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
    for frameinfo in inspect.stack():
        basename = os.path.basename(frameinfo.filename)
        if basename.startswith("test_"):
            dirname = os.path.dirname(frameinfo.filename)
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


def ruff_check(filename, code=True, docs=True):
    """Run 'ruff check' on the given file.

    Args:
        filename (str): The source file to check.
        code (bool): Check for code style errors.
        docs (bool): Check for docstring errors.
    """
    chdir_test()
    if code:
        result = subprocess.run(["ruff", "check", filename, "--config", _get_cfg("ruff-code.toml")],
                                capture_output=True, text=True)
        if result.returncode:
            pytest.fail("\n".join("  " + line for line in result.stdout.splitlines()), False)
    if docs:
        result = subprocess.run(["ruff", "check", filename, "--config", _get_cfg("ruff-docs.toml")],
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


def submission_open(before=5, after=5):
    """Check if the current time is within the user's submission window.

    The window starts at the release date and ends at the due date (or late
    due date, if set). This function applies a tolerance by including times:
      * `before` minutes prior to the release date
      * `after` minutes beyond the due/late date

    Args:
        before (int): Minutes to extend the window before the release date.
        after (int): Minutes to extend the window after the due/late date.

    Returns:
        bool: True if the current time is within the submission window.
    """

    # Get the submission metadata
    try:
        with open("/autograder/submission_metadata.json") as file:
            metadata = json.load(file)
    except FileNotFoundError:
        return False

    # Get the assignment's dates specific to the user
    assignment = metadata["users"][0]["assignment"]
    beg = datetime.fromisoformat(assignment["release_date"])
    end = datetime.fromisoformat(assignment["due_date"])
    late = assignment.get("late_due_date")
    if late is not None:
        end = datetime.fromisoformat(late)

    # Extend the submission window
    beg -= timedelta(minutes=before)
    end += timedelta(minutes=after)

    # Compare with current time
    now = datetime.now(timezone.utc)
    return beg <= now <= end


def submission_closed():
    """Check if the current time is outside the user's submission window.

    See submission_open() for more details. This function returns the opposite.
    """
    return not submission_open()


def postpone_tests(
    title="Ready to grade",
    message="Your submission has been received and will be graded manually.",
):
    """Replace all tests in the calling test module with a single placeholder.

    This function is used to hide autograder feedback during an assignment or
    exam. It deletes all existing test functions and defines a new function
    named `test_postpone` that carries the given title and message.

    Args:
        title (str): Docstring for the new test (rendered as the test's name).
        message (str): Message assigned to the new test's `output` attribute.
    """

    # Get the test module
    for frameinfo in inspect.stack():
        module = inspect.getmodule(frameinfo.frame)
        if module and module.__name__.startswith("test_"):
            test_module = module
            break

    # Delete all test functions
    g = test_module.__dict__
    for name in list(g.keys()):
        if name.startswith("test_"):
            del g[name]

    # Define the fallback test
    def test_postpone():
        test_postpone.__doc__ = title
        test_postpone.output = message

    g["test_postpone"] = test_postpone
