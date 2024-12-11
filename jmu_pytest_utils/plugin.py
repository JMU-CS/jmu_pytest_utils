"""Generate the final results.json file for Gradescope.

https://docs.pytest.org/en/stable/reference/reference.html
https://gradescope-autograders.readthedocs.io/en/latest/specs/
"""

import json
import os

# Initial results.json created in limit.py via run_autograder
RESULTS = None

# Map nodeid string to list of reports (setup, call, teardown)
REPORTS = {}


def pytest_sessionstart(session):
    """Read the initial results.json data."""
    if os.path.exists("results.json"):
        with open("results.json") as file:
            global RESULTS
            RESULTS = json.load(file)


def pytest_runtest_logreport(report):
    """Store a copy of each test report."""

    # Abort if not in run_autograder
    if not RESULTS:
        return

    # Add the report to the dictionary
    key = report.nodeid
    if key in REPORTS:
        REPORTS[key].append(report)
    else:
        REPORTS[key] = [report]


def pytest_sessionfinish(session, exitstatus):
    """Generate results.json at the end."""

    # Abort if not in run_autograder
    if not RESULTS:
        return

    # Summarize the test reports
    tests = []
    total = 0
    for item, reports in zip(session.items, REPORTS.values()):

        # The name is the docstring or function name
        test = {
            "name": item.function.__doc__ or item.name
        }
        tests.append(test)

        # max_score is set by the @weight() decorator
        weight = getattr(item.function, "weight", 0)
        # score can set manually for partial credit
        score = getattr(item.function, "score", 0)
        if not score:
            # The default score is all or nothing
            if all(r.passed for r in reports):
                score = weight
            else:
                score = 0
        # Show score only if not 0/0 points (blue)
        if score or weight:
            total += score
            test["score"] = score
            test["max_score"] = weight

        # Extract output lines that start with "E"
        output = getattr(item.function, "output", "")
        for r in reports:
            for line in r.longreprtext.splitlines():
                if line.startswith("E       "):
                    output += "\n" + line[8:]
        output = output.strip()
        if output:
            test["output"] = output

        # If the test was required, stop here
        required = getattr(item.function, "required", None)
        if required and any(r.failed for r in reports):
            output += "\n\nThis test must pass before other results are shown."
            test["output"] = output
            test["status"] = "failed"
            break

    # Write the results.json file
    RESULTS["tests"] = tests
    RESULTS["score"] = total
    with open("results.json", "w") as file:
        json.dump(RESULTS, file, indent=4)
