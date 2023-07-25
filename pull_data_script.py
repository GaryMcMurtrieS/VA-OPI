"""Script that is run when data is requested to be pulled."""

import datetime
import os
import subprocess
import tempfile

from org.csstudio.opibuilder.scriptUtil import PVUtil

# Get the start and end times for when PV data should be pulled as a string
time_start = PVUtil.getString(pvs[1])
time_end = (datetime.datetime.strptime(time_start[:-6], '%Y-%m-%dT%H:%M:%S.%f') +
            datetime.timedelta(minutes=15)).isoformat() + time_start[-6:]

# Command to unset pythonpath
# Necessary to get pyarchappl to function properly
unset_command = "unset PYTHONPATH"

# Create a temporary file to hold the data
with tempfile.NamedTemporaryFile() as temp_file:
    output_file = temp_file.name + ".csv"

    # Define the command to get the current time in seconds using the `date` utility
    archappl_command = [
        "pyarchappl-get", "--pv VA:FS1_BBS:BPM_D2421:PHA_RD", "--output {}".format(output_file),
        "--from {}".format(time_start), "--to {}".format(time_end), "--url http://127.0.0.1:17665"
    ]

    # Combine the unset command with your actual command
    full_command = unset_command + "; " + " ".join(archappl_command)

    # Run the command using subprocess.Popen
    process = subprocess.Popen(full_command, shell=True)
    process.wait()

    # Read the data from the CSV file
    with open(output_file) as csvfile:
        # Skip the header line
        next(csvfile)
        # Read the second line from the CSV file
        second_line = csvfile.readline()
        # Split the second line on comma (`,`), assuming the value is in the second column
        _, historic_value = second_line.strip().split(',')
        # Strip any leading/trailing spaces from the extracted value
        historic_value = historic_value.strip()

# Set the PV value
pvs[2].setValue(historic_value)
