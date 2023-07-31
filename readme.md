# Plan for Developing OPI for Virtual Accelerator

1. Read and understand the .lat file of the LS1FS1 virtual accelerator (VA)
2. Understand how the VA works, how to get the readings and how to change the device settings
3. Build OPIs to list all the device settings by types, e.g. one screen for correctors, one for cavities, etc.
4. Build OPIs to list all diagnostic device readings, e.g. beam position monitors (BPMs), and try to use chart widget to visualize the data
5. [Optional] Try to build the synoptic view of the VA, this is a bonus item, but is also a good chance to extend the graphical drawing capabilities for opi-generator.

### To-do

- Add additional label for number of PVs that were successfully retrieved
- Add button to view data in pop-up window - CS-Studio Array?
- Add indicator whether all data has been imported correctly
- Add set data button
- Change precision of displays to fixed value (5)
- Change XYGraph to be more generic and have bar graph in Contrib
- Display historic data in read only boxes
- Display timestamp of when data was changed
- Input and set for archive data
- LED **with label** that is green when currently displayed time travel data matches the timestamp
- Manually set fonts for boxes
- Merge CAV and SOL tabs
- Push button that opens text file with pulled data (either in seperate window or CS-Studio Array)
- Show column units in header not values
- Side-by-Side view for Historic and modern data
- When in time travel, set text color to be blue

Resample?

https://github.com/users/zhangt58/projects/1
