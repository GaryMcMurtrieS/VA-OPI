# Plan for Developing OPI for Virtual Accelerator

1. Read and understand the .lat file of the LS1FS1 virtual accelerator (VA)
2. Understand how the VA works, how to get the readings and how to change the device settings
3. Build OPIs to list all the device settings by types, e.g. one screen for correctors, one for cavities, etc.
4. Build OPIs to list all diagnostic device readings, e.g. beam position monitors (BPMs), and try to use chart widget to visualize the data
5. [Optional] Try to build the synoptic view of the VA, this is a bonus item, but is also a good chance to extend the graphical drawing capabilities for opi-generator.

### To-do

- Add button to view data in pop-up window - CS-Studio Array?
- Add functionality to restore historic data
- Add indicator whether all data has been imported correctly
- Add set data button
- Change XYGraph to be more generic and have bar graph in Contrib
- Display historic data in read only boxes
- Display timestamp of when data was changed
- Input and set for archive data
- Side-by-Side view for Historic and modern data
- Time-Travel Mode (Use Rules for TextUpdate boxes)
- Use temp file to store data

Resample?

https://github.com/users/zhangt58/projects/1

Alright, I have a more complex issue I need help with.

This script works great as a proof of concept, but I need to expand it substantially. In my code, I have several tabs, where each tab has a separate button that runs a script. Each script needs to not pull just one PV, but an entire LIST of PVs, and set a bunch of PVs to have those values. How can I accomplish this?
