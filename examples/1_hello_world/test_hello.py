from jmu_pytest_utils.common import run_module
from jmu_pytest_utils.decorators import weight


@weight(10)
def test_output():
    stdout = run_module("hello.py")
    assert stdout == "Hello, World!\n"
