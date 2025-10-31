"""Functions that use the submission metadata."""

from datetime import datetime, timedelta, timezone
import inspect
import json


def _load_user() -> dict | None:
    """Load submission metadata and get the first user.

    Returns:
        JSON object with id, email, name, sid, assignment, and sections.
        None if submission_metadata.json is not found (running offline).
    """
    try:
        with open("/autograder/submission_metadata.json") as file:
            metadata = json.load(file)
            return metadata["users"][0]
    except FileNotFoundError:
        return None
    except IndexError as e:
        raise IndexError("user not found in submission metadata") from e


def get_username(default: str = "username") -> str:
    """Get the student's username from the submission metadata.

    Args:
        default: Value to return if metadata not found.

    Returns:
        The student's email address before the @ symbol.
    """
    user = _load_user()
    if user is None:
        return default
    return user["email"].split("@")[0]


def submission_open(before: int = 5, after: int = 5) -> bool:
    """Check if the current time is within the user's submission window.

    The window starts at the release date and ends at the due date (or late
    due date, if set). This function applies a tolerance by including times:
      * `before` minutes prior to the release date
      * `after` minutes beyond the due/late date

    Args:
        before: Minutes to extend the window before the release date.
        after: Minutes to extend the window after the due/late date.

    Returns:
        True if the current time is within the submission window.
    """
    user = _load_user()
    if user is None:
        return False

    # Get the assignment's dates specific to the user
    assignment = user["assignment"]
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


def submission_closed() -> bool:
    """Check if the current time is outside the user's submission window.

    Returns:
        The opposite of `submission_open()` with default arguments.
    """
    return not submission_open()


def postpone_tests(
    title: str = "Ready to grade",
    message: str = "Your submission has been received and will be graded manually.",
) -> None:
    """Replace all tests in the calling test module with a single placeholder.

    This function is used to hide autograder feedback during an assignment or
    exam. It deletes all existing test functions and defines a new function
    named `test_postpone` that carries the given title and message.

    Args:
        title: Docstring for the new test (rendered as the test's name).
        message: Message assigned to the new test's `output` attribute.
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
