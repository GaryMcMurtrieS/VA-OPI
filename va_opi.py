from opigen import Renderer
from opigen import widgets
from opigen.contrib import Display
from opigen.contrib import TextEntry
from opigen.contrib import TextUpdate

# Variables to control widget positioning
filename = "va_opi"
box_height = 25
horizontal_gap = 5
vertical_gap = 5
name_width = 150
data_width = 700

# Reads in data from file
raw_data = open("VA_pvlist.txt", "r", encoding='utf-8').readlines()

# Creates a dictionary for each type, that maps to a dictionary for each name with entries for each
# widget that must be created.
pv_data = {}
for line in raw_data:
    line = line.rstrip()

    # Strips numbers from the type, so they can be grouped together
    device_type = ''.join(ch for ch in line.split(":")[2].split("_")[0] if not ch.isdigit())

    name = ":".join(line.split(":")[1:3])

    pv_data.setdefault(device_type, {}).setdefault(name, []).append(line)

# Sets up screen
screen = Display(800, 600, "Virtual Accelerator")

# Creates the tab container to hold all the various monitors
x0 = horizontal_gap
y0 = vertical_gap
tab_container = widgets.TabbedContainer(x0, y0, name_width + data_width + 10, box_height * 30)
screen.add_child(tab_container)

# Gets all the types and sorts them
device_types = list(pv_data)
device_types.sort()

# Creates a tab for each type of monitor
for device_type in device_types:
    y0 = vertical_gap

    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0, name_width + data_width, box_height * 29,
                                           device_type)

    # Gets names of columns to be shown
    column_names = sorted(
        [i.split(":")[-1] for i in pv_data[device_type][next(iter(pv_data[device_type]))]])
    column_count = len(column_names)
    column_width = (data_width / column_count) - horizontal_gap

    # Creates all the widgets for column name labels
    x0 = horizontal_gap + name_width + horizontal_gap
    for column_name in column_names:
        column_label = widgets.Label(x0, y0, column_width, box_height, column_name)
        tab_widget.add_child(column_label)
        x0 += column_width + horizontal_gap
    y0 += box_height + vertical_gap

    # This goes through each actual device that is of type device type
    for device in pv_data[device_type]:
        x0 = horizontal_gap

        # First, the label is created and added with the device ID
        device_label = widgets.Label(x0, y0, name_width, box_height, device)
        tab_widget.add_child(device_label)

        x0 += name_width + horizontal_gap

        # Next, each of that devices parameters is added as a widget
        # CSET parameters can take text input and be changed, everything else cannot be changed
        # and only read back
        for parameter in sorted(pv_data[device_type][device]):
            if parameter.endswith("CSET"):
                parameter_output = TextEntry(x0, y0, column_width, box_height, parameter)
            else:
                parameter_output = TextUpdate(x0, y0, column_width, box_height, parameter)

            tab_widget.add_child(parameter_output)
            x0 += column_width + horizontal_gap

        y0 += box_height + vertical_gap

    # Once all widgets are added to the container for the tab, the tab is created and the widget is
    # added to it
    tab_container.add_tab(device_type, tab_widget)

# Outputs to file
r = Renderer(screen)
r.to_opi(f"{filename}.opi")
r.to_bob(f"{filename}.bob")
