# Plan for Developing OPI for Virtual Accelerator

1. Read and understand the .lat file of the LS1FS1 virtual accelerator (VA)
2. Understand how the VA works, how to get the readings and how to change the device settings
3. Build OPIs to list all the device settings by types, e.g. one screen for correctors, one for cavities, etc.
4. Build OPIs to list all diagnostic device readings, e.g. beam position monitors (BPMs), and try to use chart widget to visualize the data
5. [Optional] Try to build the synoptic view of the VA, this is a bonus item, but is also a good chance to extend the graphical drawing capabilities for opi-generator.

### To-do

- Add functionality to restore historic data
- Change XYGraph to be more generic and have bar graph in Contrib
- Display historic data in read only boxes
- Input and set for archive data
- Time-Travel Mode (Use Rules for TextUpdate boxes)

Use subproccess.run to invoke external scripts?



javapython

run external script


cpython

create dataframe
save to csv / return dataframe

command line tools

dump out dictionary? - serialize to json string


jpython

import data?
read data from file?
import dictionary / json


https://github.com/users/zhangt58/projects/1
