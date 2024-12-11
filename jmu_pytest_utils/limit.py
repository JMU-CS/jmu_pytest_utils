"""Initialize results.json with submission metadata."""

from datetime import datetime
import json
import os
import sys

import pytz
TZ = pytz.timezone(os.getenv("SCHOOL_TIME_ZONE"))


def main():
    """Called by run_autograder to enforce the submission limit."""

    try:
        with open("/autograder/submission_metadata.json") as file:
            data = json.load(file)
            # Get the timestamp in local time zone
            stamp = datetime.fromisoformat(data["created_at"])
            stamp = stamp.astimezone(TZ)
            # Get the list of previous submissions
            prev = data["previous_submissions"]
    except FileNotFoundError:
        stamp = datetime.now()
        prev = []

    # Ignore submissions that don't count
    total = 1 + len(prev)
    for submit in prev:
        try:
            # See results at the end of this function
            submit["results"]["extra_data"]["valid_files"]
        except (KeyError, TypeError):
            total -= 1

    # Format results for printing
    stamp = stamp.strftime("%b %d at %H:%M:%S")

    # Check submission limit
    status = 0
    limit = int(os.getenv("SUBMISSION_LIMIT"))
    if limit < 0:
        output = f"Submission {total} of unlimited -- {stamp}"
    else:
        output = f"Submission {total} of {limit} -- {stamp}"
        if total > limit:
            output += "\n\n" \
                + "Limit exceeded. Please click the Submission History button " \
                + "and activate the submission you would like to be graded."
            status = 1

    # Write results.json for use in plugin.py
    results = {
        "extra_data": {"valid_files": True},
        "output": output,
        "score": 0,
    }
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)

    # Notify run_autograder whether to proceed
    sys.exit(status)


if __name__ == "__main__":
    main()
