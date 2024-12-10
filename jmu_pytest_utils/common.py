"""Common test functions used in many assignments."""

import inspect
import os
import subprocess

# Automatically change to the directory of the test module
# so that tests can run both in VS Code and on Gradescope.
for frame_info in inspect.stack()[1:]:
    module = inspect.getmodule(frame_info.frame)
    if module and "/lib/" not in module.__file__:
        os.chdir(os.path.dirname(os.path.abspath(module.__file__)))
        break


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
    result = subprocess.run(["flake8", "--config=" + _get_cfg("flake8.cfg"), filename],
                            capture_output=True, text=True)
    assert result.returncode == 0, "PEP 8 issues:\n" + \
        "\n".join("  " + line for line in result.stdout.splitlines())


def assert_docs(filename):
    """Run flake8 with docstring.cfg on the given file.

    Args:
        filename (str): The source file to check.
    """
    result = subprocess.run(["flake8", "--config=" + _get_cfg("docstring.cfg"), filename],
                            capture_output=True, text=True)
    assert result.returncode == 0, "Docstring issues:\n" + \
        "\n".join("  " + line for line in result.stdout.splitlines())


def run_module(filename, input=""):
    """Run the given module in a subprocess.

    Args:
        filename (str): The source file to run.
        input (str): Standard input from the user.

    Returns:
        CompletedProcess: Captured stdout and stderr.
    """
    return subprocess.run(["python", filename], input=input, capture_output=True, text=True)
