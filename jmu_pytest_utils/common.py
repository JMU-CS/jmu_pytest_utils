"""Common test functions used in many autograders."""

import builtins
import inspect
import io
import os
import pytest
import subprocess
import sys


def chdir_test() -> None:
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


def _get_cfg(filename: str) -> str:
    """Get the path of an optional configuration file.

    Args:
        filename: Config file (Ex: "flake8.cfg").

    Returns:
        Relative or absolute path to config file.
    """
    if os.path.exists(filename):
        return filename
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, "template", filename)


def assert_pep8(filename: str) -> None:
    """Run flake8 with flake8.cfg on the given file.

    Args:
        filename: The source file to check.
    """
    chdir_test()
    result = subprocess.run(["flake8", "--config=" + _get_cfg("flake8.cfg"), filename],
                            capture_output=True, text=True)
    if result.returncode:
        pytest.fail("PEP 8 issues:\n" + "\n".join("  " +
                    line for line in result.stdout.splitlines()), False)


def assert_docs(filename: str) -> None:
    """Run flake8 with docstring.cfg on the given file.

    Args:
        filename: The source file to check.
    """
    chdir_test()
    result = subprocess.run(["flake8", "--config=" + _get_cfg("docstring.cfg"), filename],
                            capture_output=True, text=True)
    if result.returncode:
        pytest.fail("Docstring issues:\n" + "\n".join("  " +
                    line for line in result.stdout.splitlines()), False)


def ruff_check(filename: str, code: bool = True, docs: bool = True) -> None:
    """Run 'ruff check' on the given file.

    Args:
        filename: The source file to check.
        code: Check for code style errors.
        docs: Check for docstring errors.
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


def run_command(args: list[str], user_input: str | None = None) -> str:
    """Run the given command in a subprocess.

    Args:
        args: The command (and args) to run.
        user_input: Lines of input (separated by `\\n`) from the user.

    Returns:
        Captured output from the child process.
    """
    chdir_test()
    result = subprocess.run(args, input=user_input, capture_output=True, text=True)
    if result.stderr:
        # remove absolute paths from the traceback
        reason = result.stderr.replace(os.getcwd() + os.path.sep, "")
        pytest.fail(reason, False)
    return result.stdout


def run_module(filename: str, user_input: str | None = None) -> str:
    """Run the given module in a subprocess.

    Args:
        filename: The source file to run.
        user_input: Lines of input (separated by `\\n`) from the user.

    Returns:
        Captured output from the child process.
    """
    return run_command(["python", filename], user_input)


def _input(prompt: str | None = None) -> str:
    """Read a line of input from stdin, writing the prompt to stderr.

    Args:
        prompt: Optional prompt string to display before reading input.

    Returns:
        The next line of input from stdin, with the trailing newline removed.

    Raises:
        EOFError: If no more input is available from stdin.
    """
    if prompt:
        # show prompt on stderr without adding a newline
        sys.stderr.write(prompt)
        sys.stderr.flush()
    line = sys.stdin.readline()
    if line == "":
        # mirror input()'s behavior when stdin is exhausted
        raise EOFError
    return line[:-1] if line.endswith("\n") else line


class redirect_stdin:
    """Context manager that temporarily redirects standard input.

    While active, the built-in input() function is replaced with a wrapper that
    writes the prompt to stderr, so that prompts stay separate from the output.

    Args:
        user_input: Lines of input (separated by `\\n`) from the user.
    """

    def __init__(self, user_input: str) -> None:
        self._old_input = None
        self._old_stdin = None
        self._user_input = user_input

    def __enter__(self):
        self._old_input = builtins.input
        self._old_stdin = sys.stdin
        builtins.input = _input
        sys.stdin = io.StringIO(self._user_input)

    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.input = self._old_input
        sys.stdin = self._old_stdin
        if exc_type is EOFError:
            pytest.fail("EOFError: input() was called too many times")
