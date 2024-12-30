# History

For [CS 149][1] at JMU, we used [jmu_gradescope_utils][2] to build autograders for most assignments from Spring 2022 to Fall 2024.
During this time, we transitioned from [unittest][3] to [pytest][4] for teaching students how to write their own tests.
While students used pytest for assignments, faculty relied on unittest for autograders, which led to some confusion.
Faculty also duplicated code in autograders for tasks like checking required files and enforcing submission limits.
We faced additional challenges with the underlying [gradescope-utils][5] library, such as partial credit not working.
To address these issues, we wrote [jmu_pytest_utils][6] as an independent package.
`jmu_pytest_utils` simplifies autograder development and takes full advantage of pytest's advanced features.
Related libraries include:

* https://github.com/GRudolph/autograder_samples/tree/master/python3-pytest
* https://github.com/ucsb-gradescope-tools/sample-python-pytest-autograder

[1]: https://w3.cs.jmu.edu/cs149/f24/
[2]: https://github.com/JMU-CS/jmu_python_gradescope_utils
[3]: https://docs.python.org/3/library/unittest.html
[4]: https://docs.pytest.org/en/stable/
[5]: https://github.com/gradescope/gradescope-utils
[6]: https://github.com/JMU-CS/jmu_pytest_utils

## Project Goals

* Use `pytest` instead of (or in addition to) `unittest`
* Be able to run tests before deploying to Gradescope
* Eliminate the need for config.ini files and directories
* Automate test_submitted_files and submission limit
* Eliminate the need for try-except importing modules
* Fix security issues including student output visibility
* Single library for autograding student's code & tests

*Not yet finished:*

* Multi-part assignments, each with its own config.sh
* Reject use of language features from later chapters


## Features

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
