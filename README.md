# jmu_pytest_utils

This package is a [pytest plugin][1] for building and running Gradescope autograders.
The code is based somewhat on [jmu_gradescope_utils][2] and [gradescope-utils][3].

Installation:

    pip install git+https://github.com/JMU-CS/jmu_pytest_utils.git

See the [examples](examples) directory for documentation and test assignments.
To build `autograder.zip`, run this command from an assignment's directory:

    jmu_pytest_utils build

[1]: https://docs.pytest.org/en/stable/how-to/plugins.html
[2]: https://github.com/JMU-CS/jmu_python_gradescope_utils
[3]: https://github.com/gradescope/gradescope-utils


## Project Goals

We used `jmu_gradescope_utils` from Spring 2022 to Fall 2024 for most CS 149 assignments.

* Use `pytest` instead of (or in addition to) `unittest`
* Be able to run tests before deploying to Gradescope
* Eliminate the need for config.ini files and directories
* Automate test_submitted_files and submission limit
* Eliminate the need for try-except importing modules
* Fix security issues including student output visibility
* Single library for autograding student's code+tests

*Not yet finished:*

* Multi-part assignments, each with its own config.sh
* Reject use of language features from later chapters


## Features

Here is a list of minor differences between `jmu_pytest_utils` and `jmu_gradescope_utils`.

* Installs the same Python version as in the computer labs
* Runs Python within a virtual environment for consistency
* Checks for required and extra files before running tests
* Submission limit in config enforced before running tests
* Automatically changes directory to the file being graded
* Test name defaults to the function name if no docstring
* Partial credit by setting the test_function.score attribute
* Custom output by setting test_function.output attribute
* Test functions automatically time out (default 5 seconds)
* Output is hidden (student can't print the test arguments)
* Security audit to prevent students from using the network
* Command-line script for building autograder.zip archives

*Not yet implemented:*

* Regular expression check (Ex: count number of comments)


## Related Work

* https://github.com/GRudolph/autograder_samples/tree/master/python3-pytest
* https://github.com/ucsb-gradescope-tools/sample-python-pytest-autograder
