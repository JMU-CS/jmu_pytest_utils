# jmu_pytest_utils

This package is a [pytest plugin][1] for building and running Gradescope autograders.
The code is based somewhat on [jmu_gradescope_utils][2] and [gradescope-utils][3].

Installation:

    pip install git+https://github.com/JMU-CS/jmu_pytest_utils.git

See the [examples](examples) directory for documentation and test assignments.
To build `autograder.zip`, run this command from an assignment's directory:

    jmu_pytest_utils build

[1]: https://docs.pytest.org/en/stable/how-to/plugins.html
[2]: https://github.com/JMU-CS/jmu_python_gradescope_utils/
[3]: https://github.com/gradescope/gradescope-utils


## Goals

* Use `pytest` instead of (or in addition to) `unittest`
* Be able to run tests before deploying to Gradescope
* Eliminate the need for config files and directories
* Automate test_submitted_files and submission limit
* Eliminate the need to try-except importing modules
* Fix issues with showing student output and security
* Single library for autograding student's code+tests

*Not yet finished:*

* Multi-part assignments, each with its own config.sh
* Prevent topics from "later" chapters (based on ast)


## Features

* Installs the same Python version as in the computer labs
* Runs Python within a virtual environment for consistency
* Checks for required and extra files before running tests
* Submission limit in config enforced before running tests
* Automatically changes directory to the file being graded
* Test name defaults to the function name if no docstring
* Partial credit by setting test_function.score attribute
* Custom output by setting test_function.output attribute
* Test functions automatically time out (default 5 seconds)
* Output is hidden (student can't print the test arguments)
* Security audit to prevent students from using the network
* Command-line script for building autograder.zip archives
* Test for correctness and code coverage of student's tests

*Not yet implemented:*

* Regular expression check (Ex: count number of comments)


## Related Work

* https://github.com/GRudolph/autograder_samples/tree/master/python3-pytest
* https://github.com/ucsb-gradescope-tools/sample-python-pytest-autograder
