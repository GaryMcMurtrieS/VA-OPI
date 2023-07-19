"""Script that is run when data is requested to be pulled."""

import java.io.BufferedReader
import java.io.InputStreamReader
from java.lang import ProcessBuilder
from org.csstudio.opibuilder.scriptUtil import PVUtil
from java.io import File
from java.io import FileReader

# Define the command to get the current time in seconds using the `date` utility
command = [
    "pyarchappl-get", "--pv VA:LS1_WA02:BPM_D1188:ENG_RD", "--from 2023-07-07T15:00:20.00-04:00",
    "--to 2023-07-07T15:10:20.00-04:00", "--url http://127.0.0.1:17665"
]

# Create a ProcessBuilder
process_builder = ProcessBuilder(["echo", "3"])

# Start the process
process = process_builder.start()

# Wait for the process to finish
process.waitFor()

# # Open the output file
# file = File("archive_data.csv")
# file_reader = FileReader(file)
# buffered_reader = BufferedReader(file_reader)

# # Read all lines from the output and find the last non-empty line
# last_line = None
# line = buffered_reader.readLine()
# while line is not None:
#     if line.strip():  # if line is not empty
#         last_line = line
#     line = buffered_reader.readLine()

# # Close the file
# buffered_reader.close()

# # Extract the last value
# if last_line is not None:
#     external_value = last_line.split(",")[-1]  # get the last element from the split line

# Get the output stream of the process
output_stream = process.getInputStream()

# Create a BufferedReader for the output stream
reader = java.io.BufferedReader(java.io.InputStreamReader(output_stream))

# Read the output from the process
external_value = reader.readLine()

# Set the PV value
pvs[2].setValue(external_value)
