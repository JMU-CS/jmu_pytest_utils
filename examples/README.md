# Examples

The following "assignments" are used for testing `jmu_pytest_utils` and provided as examples for writing your own autograders:

* [1_hello_world](1_hello_world) -- minimal example
* [2_basic_input](2_basic_input) -- program with user input
* [3_extra_credit](3_extra_credit) -- custom output and score
* [4_substitution](4_substitution) -- variable from autograder
* [5_import_funcs](5_import_funcs) -- module with functions
* [6_provided_data](6_provided_data) -- file I/O assignment
* [7_class_package](7_class_package) -- classes and packages
* [8_test_coverage](8_test_coverage) -- grading student's tests
* [9_leaderboard](9_leaderboard) -- Gradescope leaderboard

## API Docs

The [API documentation](https://jmu-cs.github.io/jmu_pytest_utils/) is automatically built with [pdoc](https://pdoc.dev/) whenever there are new commits on the main branch.

## Configuration

During autograder setup, a configuration script named [`config.sh`](../jmu_pytest_utils/template/config.sh) is automatically generated.
This script sets the environment variables used by [`run_autograder`](../jmu_pytest_utils/template/run_autograder) and other grading scripts.

You can override the default values in `config.sh` by defining global variables with the same names.
For example, you can add any of the following lines to your test module after the `import` statements:

* Limit the number of submissions:
    ``` py
    SUBMISSION_LIMIT = 10
    ```
* Change pytest's --timeout value:
    ``` py
    FUNCTION_TIMEOUT = 10
    ```
* Specify packages to be installed:
    ``` py
    REQUIREMENTS_TXT = ["beautifulsoup4", "requests"]
    ```

Alternatively, you can define environment variables that apply to *all* assignments.
For example, you can export these variables before running `jmu_pytest_utils build`:

* Change the submission time zone:
    ``` sh
    export SCHOOL_TIME_ZONE="US/Mountain"
    ```
* Install a specific python version:
    ``` sh
    export INSTALL_PYTHON_V="3.14"
    ```

The [`builder.py`](../jmu_pytest_utils/builder.py) script automatically detects assignment files using `os.walk()`.
However, you can manually override the file requirements if needed.
For example:

* Files the student must submit:
    ``` py
    SUBMISSION_FILES = ["file1.py", "file2.py"]
    ```
* Reference tests for grading:
    ``` py
    AUTOGRADER_TESTS = ["test_file1.py", "test_file2.py"]
    ```
* Other files included in zip:
    ``` py
    ADDITIONAL_FILES = ["data/hello.txt", "data/world.txt"]
    ```

When looking at `config.sh`, note that Bash and Python represent a list of files differently.
Bash uses a space-delimited string (Ex: `"file1.py file2.py"`), but Python uses a list of strings.


## Possible Results

The [`run_autograder`](../jmu_pytest_utils/template/run_autograder) script initially performs the following checks initially.
If any of these checks fail, the assignment receives 0 points, and the submission does not count toward the limit.

* Missing Files -- were all required files submitted?
* Extra Files -- were any unneeded files submitted?
* Compiler Error -- does submitted code compile?
* Security Audit -- are forbidden functions used?
* Submission Limit -- is this submission allowed?

The last step of `run_autograder` is to run `pytest`, which generates the `results.json` file required for Gradescope.
Each test function has the following possible outcomes:

* An error is raised -- no points
* An assertion fails -- no points
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
