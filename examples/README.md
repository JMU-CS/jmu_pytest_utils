# Examples

The following assignments are provided for testing `jmu_pytest_utils`:

* [1_hello_world](1_hello_world) -- minimal example
* [2_basic_input](2_basic_input) -- demos user input
* [3_extra_credit](3_extra_credit) -- custom output and score
* [4_substitution](4_substitution) -- variable from autograder
* [5_import_funcs](5_import_funcs) -- import and test functions
* [6_provided_data](6_provided_data) -- file I/O assignment
* 7_two_packages -- TODO
* 8_multiple_parts -- TODO


## Configuration

During autograder setup, a configuration script named [`config.sh`](../jmu_pytest_utils/template/config.sh) is automatically generated.
This script sets the environment variables used by [`run_autograder`](../jmu_pytest_utils/template/run_autograder) and other grading scripts.
You can override the default values in `config.sh` by defining global variables with the same names.
For example, to limit the number of submissions (unlimited by default), you can add the following line to your test module (after the `import` statements):

``` py
SUBMISSION_LIMIT = 10
```

The [`builder.py`](../jmu_pytest_utils/builder.py) script automatically detects assignment files using `os.walk()`.
However, you can manually override the file requirements if needed.
For example, to specify the only files that students must submit, add a line like this to your test module:

``` py
SUBMISSION_FILES = ["file1.py", "file2.py"]
```

When looking at `config.sh`, note that Bash and Python represent the list of files differently.
Bash uses a space-delimited string (Ex: `"file1.py file2.py"`), but Python uses a list of strings.


## Documentation

Please refer to the docstrings in the files below.

Most tests will import the following two modules:

* [`jmu_pytest_utils.common`](../jmu_pytest_utils/common.py)
* [`jmu_pytest_utils.decorators`](../jmu_pytest_utils/decorators.py)

Tests that analyze the student's *code* also import:

* [`jmu_pytest_utils.audit`](../jmu_pytest_utils/audit.py)

And of course, you will often import `pytest`:

* [API Reference - pytest documentation](https://docs.pytest.org/en/stable/reference/reference.html)


## Possible Results

The [`run_autograder`](../jmu_pytest_utils/template/run_autograder) script initially performs the following checks.
If any of these checks fail, the assignment receives 0 points, and the submission does not count toward the limit.

* Missing Files -- were all required files submitted?
* Extra Files -- were unnecessary files submitted?
* Compiler Error -- does submitted code compile?
* Security Audit -- are forbidden functions used?
* Submission Limit -- is this submission allowed?

The last step of `run_autograder` is to run `pytest`, which generates the `results.json` file required for Gradescope.
Each test function has the following possible outcomes:

* An assertion fails -- no points
* An error is raised -- no points
* The test times out -- no points
* The test is skipped -- full points
* The test passes -- full points

Each test function has optional attributes named `output` and `score`.
You can override the default outcome by setting these attributes.
For example, to give partial credit:

``` py
@weight(4)
def test_example():
    test_example.output = "Half credit for trying!"
    test_example.score = 2
```
