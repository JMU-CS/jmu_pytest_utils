"""Functions that use the submission metadata."""

from datetime import datetime, timedelta, timezone
import inspect
import json


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
