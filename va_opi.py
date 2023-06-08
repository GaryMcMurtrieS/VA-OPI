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
label_width = 150
data_width = 700

# Reads in data from file
raw_data = open("VA_pvlist.txt", "r", encoding='utf-8').readlines()

# Creates a dictionary for each type, that maps to a dictionary for each name with entries for each
# widget that must be created.
data = {}
for line in raw_data:
    line = line.rstrip()

    # Strips numbers from the type, so they can be grouped together
    component_type = ''.join(ch for ch in line.split(":")[2].split("_")[0]
                             if not ch.isdigit())

    name = ":".join(line.split(":")[1:3])

    data.setdefault(component_type, {}).setdefault(name, []).append(line)

# Sets up screen
screen = Display(800, 600, "Virtual Accelerator")

# Creates the tab container to hold all the various monitors
x0 = horizontal_gap
y0 = vertical_gap
tab_container = widgets.TabbedContainer(x0, y0, label_width + data_width + 10,
                                        box_height * 30)
screen.add_child(tab_container)

# Gets all the types and sorts them
component_types = list(data)
component_types.sort()

# Creates a tab for each type of monitor
for component_type in component_types:
    y0 = vertical_gap

    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0, label_width + data_width,
                                           box_height * 29, component_type)

    # Gets all the column names to be shown
    column_names = sorted([
        i.split(":")[-1]
        for i in data[component_type][next(iter(data[component_type]))]
    ])
    column_count = len(column_names)

    # Creates widget labels for all the column names
    x0 = horizontal_gap + label_width + horizontal_gap
    for column in column_names:
        column_label = widgets.Label(
            x0, y0, data_width / column_count - horizontal_gap, box_height,
            column)
        tab_widget.add_child(column_label)

        x0 += data_width / column_count

    y0 += box_height + vertical_gap

    # This goes through each monitor and adds them to the tab
    for monitor in data[component_type]:
        label = widgets.Label(horizontal_gap, y0, label_width, box_height,
                              monitor)
        tab_widget.add_child(label)

        x0 = horizontal_gap + label_width + horizontal_gap

        for child in sorted(data[component_type][monitor]):
            # Boxes for the child widgets are resized to fill horizontally
            if child[-4:] == "CSET":
                child_widget = TextEntry(
                    x0,
                    y0,
                    data_width / column_count - horizontal_gap,
                    box_height,
                    child,
                )
            else:
                child_widget = TextUpdate(
                    x0,
                    y0,
                    data_width / column_count - horizontal_gap,
                    box_height,
                    child,
                )

            tab_widget.add_child(child_widget)
            x0 += data_width / column_count

        y0 += box_height + vertical_gap

    tab_container.add_tab(component_type, tab_widget)

# Outputs to file
r = Renderer(screen)
r.to_opi(f"{filename}.opi")
r.to_bob(f"{filename}.bob")
