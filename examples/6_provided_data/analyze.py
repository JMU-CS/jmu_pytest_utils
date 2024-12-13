"""Sample assignment that reads and writes files."""

import csv


def count_iris(filename):
    """Count how many flowers of each species are in the iris data.

    Args:
        filename (str): Path to the iris data.

    Returns:
        dict: Maps species to counts.
    """
    result = {}
    with open(filename, newline="") as file:
        file.readline()  # csv header
        data = csv.reader(file)
        for row in data:
            species = row[-1]
            if species in result:
                result[species] += 1
            else:
                result[species] = 1
    return result


def filter_adult(src, dst):
    """Find all rows with Federal-gov and Doctorate in the adult data.

    This function reads the data from one file and saves the resulting
    rows in another file.

    Args:
        src (str): Path of the file to read.
        dst (str): Path of the file to write.
    """
    with open(src, "r", newline="") as file1, \
            open(dst, "w", newline="") as file2:
        # copy the csv header
        reader = csv.reader(file1)
        writer = csv.writer(file2)
        writer.writerow(next(reader))
        # copy the matching rows
        for row in reader:
            if row[1] == "Federal-gov" and row[3] == "Doctorate":
                writer.writerow(row)
