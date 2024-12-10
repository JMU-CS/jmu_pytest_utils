# This file is used by jmu_pytest_utils to define environment variables for
# run_autograder and related Python scripts.


# Files the student must submit
# Example: "hello.py world.py"
# Default: blank
export SUBMISSION_FILES="{0}"

# Reference tests for grading
# Example: "test_hello.py test_world.py"
# Default: blank
export AUTOGRADER_TESTS="{1}"

# Other files included in zip
# Example: "data/hello.txt data/world.txt"
# Default: blank
export ADDITIONAL_FILES="{2}"

# Max submissions that can run
# Default: -1
export SUBMISSION_LIMIT="{3}"

# Max seconds per test function
# Default: 10
export FUNCTION_TIMEOUT="{4}"

# Time zone for submissions
# Default: US/Eastern
export SCHOOL_TIME_ZONE="{5}"
