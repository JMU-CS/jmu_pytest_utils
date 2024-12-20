"""Static analysis of student code.

https://docs.python.org/3/library/ast.html#node-classes
https://saligrama.io/blog/gradescope-autograder-security/
"""

import ast
from collections import Counter
from jmu_pytest_utils.common import chdir_test
import sys


# The following modules and functions are not allowed in student code,
# because they can make the autograder vulnerable to various attacks.

MODULES = [
    # Network connections
    "asyncio",
    "ftplib",
    "http",
    "imaplib",
    "poplib",
    "smtplib",
    "socket",
    "urllib",
    # Inter-process comm
    "mmap",
    "subprocess",
    # Unit tests access
    "importlib",
    "inspect",
    "jmu_pytest_utils",
]

FUNCTIONS = [
    # Process management
    ("os", "execl"),
    ("os", "execle"),
    ("os", "execlp"),
    ("os", "execlpe"),
    ("os", "execv"),
    ("os", "execve"),
    ("os", "execvp"),
    ("os", "execvpe"),
    ("os", "fork"),
    ("os", "forkpty"),
    ("os", "popen"),
    ("os", "posix_spawn"),
    ("os", "posix_spawnp"),
    ("os", "spawnl"),
    ("os", "spawnle"),
    ("os", "spawnlp"),
    ("os", "spawnlpe"),
    ("os", "spawnv"),
    ("os", "spawnve"),
    ("os", "spawnvp"),
    ("os", "spawnvpe"),
    ("os", "startfile"),
    ("os", "system"),
]


def count_calls(filename, func_id):
    """Count how many times a function is called.

    Args:
        filename (str): The source file to parse.
        func_id (str): Function name (Ex: "print").

    Returns:
        int: Number of times the function is called.
    """
    chdir_test()
    with open(filename, encoding="utf-8") as file:
        source = file.read()
    tree = ast.parse(source, filename)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == func_id:
                count += 1
    return count


def count_nodes(filename):
    """Count the number of AST nodes in a program.

    Args:
        filename (str): The source file to parse.

    Returns:
        Counter: Maps AST node names to counts.
    """
    chdir_test()
    with open(filename, encoding="utf-8") as file:
        source = file.read()
    tree = ast.parse(source, filename)
    return Counter(type(node).__name__ for node in ast.walk(tree))


def main(paths):
    """Called by run_autograder to check for forbidden code.

    Args:
        paths (list): Names of Python source files.
    """
    def error(message):
        print(f"{path}:{node.lineno}:{node.col_offset+1} {message}")
    # parse each source file
    for path in paths:
        with open(path, encoding="utf-8") as file:
            source = file.read()
        tree = ast.parse(source, path)
        for node in ast.walk(tree):
            # look for forbidden modules
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in MODULES:
                        error(f"imports {alias.name}")
            if isinstance(node, ast.ImportFrom):
                if node.module in MODULES:
                    error(f"imports from {node.module}")
            # look for forbidden functions
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        for module, function in FUNCTIONS:
                            if node.func.value.id == module and node.func.attr == function:
                                error(f"calls {module}.{function}()")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("Usage: python audit.py file1.py file2.py ...")
