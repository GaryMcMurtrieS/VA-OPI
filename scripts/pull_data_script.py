"""Script that is run when data is requested to be pulled."""

import datetime
import subprocess
from glob import glob
from tempfile import NamedTemporaryFile as tempfile

from org.csstudio.opibuilder.scriptUtil import PVUtil

# pvs[0]: loc://$(DID)_trigger_time_travel_{device_type}
# pvs[1]: loc://$(DID)_time_{device_type}
# pvs[2]: loc://$(DID)_time_travel_{device_type}
# pvs[3]: loc://$(DID)_debug_message_{device_type}
# pvs[4]: loc://$(DID)_trigger_time_led_{device_type}

# Index at which VA PVs actually start
PV_START = 5

# Only execute script if in time travel mode
if PVUtil.getDouble(pvs[2]) == 1:
    pvs[3].setValue('Pulling data, please be patient!')

    # Get the start and end times for when PV data should be pulled as a string
    time_start = PVUtil.getString(pvs[1])
    time_end = (datetime.datetime.strptime(time_start[:-6], '%Y-%m-%dT%H:%M:%S.%f') +
                datetime.timedelta(minutes=15)).isoformat() + time_start[-6:]

    # Necessary to get pyarchappl to function properly
    unset_command = "unset PYTHONPATH"

    # Map each of the accelerator's PV to its local counterpart and create lists for both
    accelerator_pv_list = [str(pv) for pv in pvs[PV_START::2]]
    local_pv_list = pvs[PV_START + 1::2]

    # Prefix, used to check if we already ran the relevant archive command
    device_type = str(pvs[0])[str(pvs[0]).rfind('_') + 1:-3]
    prefix = "{}_{}_".format(time_start, device_type)

    for char in "-:.":
        prefix = prefix.replace(char, '')

    # Check if the archive file already exists
    existing_files = glob('/tmp/{}*'.format(prefix))
    archive_file = existing_files[0] if existing_files else None

    # If no such file exists, create a new one
    if not archive_file:
        with tempfile(prefix=prefix, delete=False) as temp_archive_file:
            archive_file = temp_archive_file.name

            # Command that actually pulls the historic data
            archappl_command = [
                "pyarchappl-get", "--from {}".format(time_start), "--to {}".format(time_end),
                "--url http://127.0.0.1:17665", "--output {}".format(archive_file)
            ] + ["--pv {}".format(pv) for pv in accelerator_pv_list]

            full_command = unset_command + "; " + " ".join(archappl_command)

            process = subprocess.Popen(full_command, shell=True)
            process.wait()

    # Read the data from the output file
    with open(archive_file) as archive_csv:
        archived_data = {}

        # Check if the file is not empty
        first_line = archive_csv.readline()
        if first_line:
            archived_pvs = first_line.strip().split(',')[1:]

            # Create a dict for all PVs that were archived
            archived_data = {pv: None for pv in archived_pvs}

            for row in archive_csv:
                archived_values = row.strip().split(',')[1:]

                # Iterate over the values and their corresponding PVs
                for archived_value, archived_pv in zip(archived_values, archived_pvs):
                    # If the value in the dict is None and this value is not an empty string, write
                    # it to the dict
                    if archived_data[archived_pv] is None and archived_value != "":
                        archived_data[archived_pv] = archived_value

        else:
            pvs[3].setValue('No Archive Data Found!')

    # Count of the found and missing PVs
    found_count = 0
    missing_count = 0

    # After reading the entire CSV file, write values or "No Data Found" to PVs
    for accelerator_pv, local_pv in zip(accelerator_pv_list, local_pv_list):
        if accelerator_pv in archived_data:
            local_pv.setValue(archived_data[accelerator_pv])
            found_count += 1
        else:
            local_pv.setValue('No Data Found!')
            missing_count += 1

    pvs[3].setValue('Data pulled. {} PV(s) loaded, {} PV(s) missing.'.format(
        found_count, missing_count))

    pvs[4].setValue(1)
