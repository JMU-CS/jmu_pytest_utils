"""A pytest plugin for building and running Gradescope autograders.

Source: https://github.com/JMU-CS/jmu_pytest_utils/

## Modules to Import

Most tests will import:

* `jmu_pytest_utils.common` – style checking and I/O support
* `jmu_pytest_utils.decorators` – `@required` and `@weight`

Some tests will import:

* `jmu_pytest_utils.audit` – analyze the student's source code
* `jmu_pytest_utils.coverage` – analyze the student's unit tests
* `jmu_pytest_utils.meta` – analyze the submission metadata

And of course `pytest`:

* [API Reference - pytest documentation](https://docs.pytest.org/en/stable/reference/reference.html)

## Command-Line Tools

Tests don't need to import:

* `jmu_pytest_utils.builder` – autograder.zip build script
* `jmu_pytest_utils.limit` – enforce the submission limit
* `jmu_pytest_utils.plugin` – pytest plugin for results.json
"""
