import time
import csv
from datetime import datetime

# Code pertains to storing data in a CSV file.
def stamper():
    # function makes a timestamp
    dt = datetime.now()
    iso_date = dt.isoformat()
    return iso_date


def write_to_csv(date, voltage):
    """
    function takes in timestamp and voltage,
    writes values to csv file,
    "a" appends whereas "w" clears file first
    """
    with open("timestamps.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([date, voltage])
        # writer.writerow("\n")


def clear_csv():
    """
    function clears csv file,
    just scaffolding for now, "w+" truncates the file
    """
    with open("timestamps.csv", "w+", newline="") as csv_file:
        pass
