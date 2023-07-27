"""Script that is run when data is requested to be pulled."""

import datetime
import subprocess
from tempfile import NamedTemporaryFile as TempFile

from org.csstudio.opibuilder.scriptUtil import PVUtil

if PVUtil.getDouble(pvs[2]) == 1:
    # Get the start and end times for when PV data should be pulled as a string
    time_start = PVUtil.getString(pvs[1])
    time_end = (datetime.datetime.strptime(time_start[:-6], '%Y-%m-%dT%H:%M:%S.%f') +
                datetime.timedelta(minutes=15)).isoformat() + time_start[-6:]

    # Necessary to get pyarchappl to function properly
    unset_command = "unset PYTHONPATH"

    pv_list = [str(pv) for pv in pvs[2:]]

    # Create a temporary file to hold the archival data
    with TempFile() as temp_archive_file:
        archive_file = temp_archive_file.name

        # Command that actually pulls the historic data
        archappl_command = [
            "pyarchappl-get", "--url http://127.0.0.1:17665", "--output {}".format(archive_file),
            "--from {}".format(time_start), "--to {}".format(time_end)
        ] + ["--pv {}".format(pv) for pv in pv_list]

        # Combine the unset command with actual command
        full_command = unset_command + "; " + " ".join(archappl_command)

        # Run the command
        process = subprocess.Popen(full_command, shell=True)
        process.wait()

        # Read the data from the output file
        with open(archive_file) as archive_csv:
            archived_pvs = next(archive_csv).strip().split(',')[1:]  # Excluding time

            # Create a dict for all PVs that were archived
            archived_data = {pv: None for pv in archived_pvs}

            for row in archive_csv:
                archived_values = row.strip().split(',')[
                    1:]  # Exclude the timestamp from the values

                # Iterate over the values and their corresponding PVs
                for archived_value, archived_pv in zip(archived_values, archived_pvs):
                    # If the value in the dict is None and this value is not an empty string, write
                    # it to the dict
                    if archived_data[archived_pv] is None and archived_value != "":
                        archived_data[archived_pv] = archived_value

    # After reading the entire CSV file, write values or "No Data Found" to PVs
    for pv in pv_list:
        if pv in archived_data:
            PVUtil.writePV("loc://time_travel_{}".format(pv), archived_data[pv])
        else:
            PVUtil.writePV("loc://time_travel_{}".format(pv), "No Data Found")
