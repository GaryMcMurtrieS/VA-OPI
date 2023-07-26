"""Script that is run when data is requested to be pulled."""

import datetime
import subprocess
from tempfile import NamedTemporaryFile as TempFile

from org.csstudio.opibuilder.scriptUtil import PVUtil

# Get the start and end times for when PV data should be pulled as a string
time_start = PVUtil.getString(pvs[1])
time_end = (datetime.datetime.strptime(time_start[:-6], '%Y-%m-%dT%H:%M:%S.%f') +
            datetime.timedelta(minutes=15)).isoformat() + time_start[-6:]

# Command to unset pythonpath
# Necessary to get pyarchappl to function properly
unset_command = "unset PYTHONPATH"

# Gets the list of PVs from a local PV
pv_list = []
for pv in pvs[2:]:
    if str(pv).startswith("VA:"):
        pv_list.append(pv)

# Create a temporary file to hold the archival data
with TempFile(delete=False, prefix="archivedata_") as temp_archive_data_file:
    # Main command that actually pulls the historic data
    archappl_command = [
        "pyarchappl-get", "--output {}".format(temp_archive_data_file.name),
        "--from {}".format(time_start), "--to {}".format(time_end), "--url http://127.0.0.1:17665"
    ]

    for pv in pv_list:
        archappl_command.append("--pv {}".format(pv))

    pvs[2].setValue(" ".join(archappl_command))

    # Combine the unset command with your actual command
    full_command = unset_command + "; " + " ".join(archappl_command)

    # Run the command using subprocess.Popen
    process = subprocess.Popen(full_command, shell=True)
    process.wait()

    # Read the data from the CSV file
    with open(temp_archive_data_file.name) as csvfile:
        # Skip the header line
        next(csvfile, None)
        # Read the second line from the CSV file
        second_line = next(csvfile, None)
        if second_line:
            # Split the second line on comma (`,`), assuming the value is in the second column
            values = second_line.strip().split(',')[1:]  # Exclude the timestamp from the values
            for i, value in enumerate(values):
                # Set the PV value to its corresponding index
                pvs[i * 2 + 3].setValue(value.strip())

        else:
            # Handle the case where the CSV file is empty or doesn't contain data
            for i in range(len(pvs[3:])):
                pvs[i * 2 + 3].setValue("No Historic Data Found")
