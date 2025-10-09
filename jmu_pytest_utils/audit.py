"""Static analysis of student code.

https://docs.python.org/3/library/ast.html#node-classes
https://saligrama.io/blog/gradescope-autograder-security/
"""

import ast
import pytest
import re
import sys
import tokenize

from collections import Counter
from jmu_pytest_utils.common import chdir_test

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


def assert_no_if(filename, main=True):
    """Check that no if statements/expressions are used.

    Args:
        filename (str): The source file to parse.
        main (bool): Don't count if __name__ == "__main__".
    """
    count = 0
    if main:
        source = get_source_code(filename)
        tree = ast.parse(source, filename)
        # Iterate top-level statements only
        for node in tree.body:
            if (
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.Eq)
                and isinstance(node.test.comparators[0], ast.Constant)
                and node.test.comparators[0].value == "__main__"
            ):
                count += 1
    node_count = count_nodes(filename)
    assert node_count["If"] == count, "If statements are not allowed"
    assert node_count["IfExp"] == 0, "If expressions are not allowed"


def assert_no_for(filename, comps=True):
    """Check that no for loops are used.

    Args:
        filename (str): The source file to parse.
        comps (bool): Also check for comprehensions and generator expressions.
    """
    node_count = count_nodes(filename)
    assert node_count["For"] == 0, "For loops are not allowed"
    if comps:
        assert_no_functional(filename)


def assert_no_while(filename):
    """Check that no while loops are used.

    Args:
        filename (str): The source file to parse.
    """
    node_count = count_nodes(filename)
    assert node_count["While"] == 0, "While loops are not allowed"


def assert_no_loops(filename):
    """Calls assert_no_for() and assert_no_while().

    Args:
        filename (str): The source file to parse.
    """
    assert_no_for(filename)
    assert_no_while(filename)


def assert_no_functional(filename):
    """Check that functional programming features are NOT used.

    This includes list/set/dict comprehensions, generator expressions, and
    lambda expressions.

    Args:
        filename (str): The source file to parse.
    """
    node_count = count_nodes(filename)
    assert node_count["ListComp"] == 0, "List comprehensions are not allowed"
    assert node_count["SetComp"] == 0, "Set comprehensions are not allowed"
    assert node_count["DictComp"] == 0, "Dict comprehensions are not allowed"
    assert node_count["GeneratorExp"] == 0, "Generator expressions are not allowed"
    assert node_count["Lambda"] == 0, "Lambda expressions are not allowed"


def assert_not_imported(filename, modules):
    """Check that forbidden modules are not imported.

    Args:
        filename (str): The source file to parse.
        modules (list): Names of modules that are not allowed to be imported.
    """
    source = get_source_code(filename)
    tree = ast.parse(source, filename)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in modules:
                    pytest.fail(f"Importing {alias.name} is not allowed")
        if isinstance(node, ast.ImportFrom):
            if node.module in modules:
                pytest.fail(f"Importing from {node.module} is not allowed")


def count_calls(filename, func_id):
    """Count how many times a function is called.

    Args:
        filename (str): The source file to parse.
        func_id (str): Function/method name (Ex: "print").

    Returns:
        int: Number of times the function is called.
    """
    source = get_source_code(filename)
    tree = ast.parse(source, filename)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # plain function calls
            if isinstance(node.func, ast.Name) and node.func.id == func_id:
                count += 1
            # method/attribute calls
            if isinstance(node.func, ast.Attribute) and node.func.attr == func_id:
                count += 1
    return count


def count_comments(filename):
    """Count the number of # comments in a program.

    Args:
        filename (str): The source file to parse.

    Returns:
        int: Number of end-of-line comments found.
    """
    count = 0
    chdir_test()
    with open(filename, encoding="utf-8") as file:
        tokens = tokenize.generate_tokens(file.readline)
        for tok_type, _, _, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                count += 1
    return count


def count_nodes(filename):
    """Count the number of AST nodes in a program.

    Some nodes that autograders often check include "If", "IfExp",
    "For", "While", "Subscript", "ListComp", "SetComp", "DictComp",
    "GeneratorExp", and "Lambda".

    See https://docs.python.org/3/library/ast.html for the complete
    list of node names.

    Args:
        filename (str): The source file to parse.

    Returns:
        Counter: Maps AST node names to counts.
    """
    source = get_source_code(filename)
    tree = ast.parse(source, filename)
    return Counter(type(node).__name__ for node in ast.walk(tree))


def count_regex_matches(filename, pattern, strip_comments=True):
    """Count the number of regex pattern matches in code.

    Args:
        filename (str): The source file to parse.
        pattern (str): Regular expression pattern to match.
        strip_comments (bool): Whether to remove comments before matching.

    Returns:
        int: Number of matches found.
    """
    source = get_source_code(filename)
    if strip_comments:
        # Parse and unparse the source code
        tree = ast.parse(source, filename)
        tree = remove_docstrings(tree)
        source = ast.unparse(tree)
    return len(re.findall(pattern, source))


def get_source_code(filename):
    """Read the contents of a source file.

    Args:
        filename (str): The source file to read.

    Returns:
        str: Contents of the source file.
    """
    chdir_test()
    with open(filename, encoding="utf-8") as file:
        return file.read()


def remove_docstrings(node):
    """Remove all docstrings from the given AST node.

    Args:
        node (AST): The root of the AST to process.

    Returns:
        AST: Same node with all docstrings removed.
    """
    places = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)
    for child in ast.walk(node):
        if isinstance(child, places):
            if (child.body
                and isinstance(child.body[0], ast.Expr)
                and isinstance(child.body[0].value, ast.Constant)
                and isinstance(child.body[0].value.value, str)
            ):
                child.body.pop(0)
    return node


def main(paths):
    """Called by run_autograder to check for forbidden code.

    Args:
        paths (list): Names of Python source files.
    """
    def error(message):
        print(f"{path}:{node.lineno}:{node.col_offset+1} {message}")
    # parse each source file
    for path in paths:
        if not path.endswith(".py"):
            continue
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
