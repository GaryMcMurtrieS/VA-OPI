""" Creates Phoebus and CS-Studio OPI Files for reading Accelerator Data"""

from opigen import Renderer
from opigen import widgets
from opigen.contrib import Display
from opigen.contrib import TextEntry
from opigen.contrib import TextUpdate

# Variables to control widget positioning
FILENAME = "va_opi"
WIDGET_HEIGHT = 25
NAME_WIDTH = 150
DATA_WIDTH = 700
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5


def data_reading():
    """Reads data and converts it to dict format for main code"""

    # Reads in data from file
    with open("VA_pvlist.txt", "r", encoding='utf-8') as file:
        raw_data = file.readlines()

    # Creates a dictionary for each type, that maps to a dictionary for each name with entries for
    # each widget that must be created.
    pv_data = {}
    for line in raw_data:
        line = line.rstrip()

        # Strips numbers from the type, so they can be grouped together
        device_type = ''.join(ch for ch in line.split(":")[2].split("_")[0] if not ch.isdigit())

        name = ":".join(line.split(":")[1:3])

        pv_data.setdefault(device_type, {}).setdefault(name, []).append(line)

    return pv_data


def create_tab_container(screen):
    """Creates and adds tab container to the screen"""
    tab_container = widgets.TabbedContainer(HORIZONTAL_GAP, VERTICAL_GAP,
                                            NAME_WIDTH + DATA_WIDTH + (3 * HORIZONTAL_GAP) + 12,
                                            SCREEN_HEIGHT + 33)
    screen.add_child(tab_container)
    return tab_container


def get_device_types(pv_data):
    """Gets all the device types and sorts them"""
    device_types = list(pv_data)
    device_types.sort()
    return device_types


def create_columns_and_get_width(pv_data, tab_widget, device_type):
    """Creates column labels for the given tab"""
    # Gets and sorts all column names
    column_names = sorted(
        [i.split(":")[-1] for i in pv_data[device_type][next(iter(pv_data[device_type]))]])
    column_count = len(column_names)
    column_width = (DATA_WIDTH / column_count) - HORIZONTAL_GAP

    # Creates all the widgets for column name labels
    x_0 = HORIZONTAL_GAP + NAME_WIDTH + HORIZONTAL_GAP
    for column_name in column_names:
        column_label = widgets.Label(x_0, HORIZONTAL_GAP, column_width, WIDGET_HEIGHT, column_name)
        tab_widget.add_child(column_label)
        x_0 += column_width + HORIZONTAL_GAP

    return column_width


def create_tab_widget(pv_data, device_type):
    """Creates the container that goes into a given tab"""
    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0,
                                           NAME_WIDTH + DATA_WIDTH + (3 * HORIZONTAL_GAP) + 10,
                                           SCREEN_HEIGHT, device_type)

    # Create column labels
    column_width = create_columns_and_get_width(pv_data, tab_widget, device_type)

    y_0 = VERTICAL_GAP + WIDGET_HEIGHT + VERTICAL_GAP

    # This goes through each actual device that is of type device type
    for device in pv_data[device_type]:
        x_0 = HORIZONTAL_GAP

        # First, the label is created and added with the device ID
        device_label = widgets.Label(x_0, y_0, NAME_WIDTH, WIDGET_HEIGHT, device)
        tab_widget.add_child(device_label)

        x_0 += NAME_WIDTH + HORIZONTAL_GAP

        # Next, each of that devices parameters is added as a widget
        # CSET parameters can take text input and be changed, everything else cannot be changed
        # and only read back
        for parameter in sorted(pv_data[device_type][device]):
            if parameter.endswith("CSET"):
                parameter_output = TextEntry(x_0, y_0, column_width, WIDGET_HEIGHT, parameter)
            else:
                parameter_output = TextUpdate(x_0, y_0, column_width, WIDGET_HEIGHT, parameter)

            tab_widget.add_child(parameter_output)
            x_0 += column_width + HORIZONTAL_GAP

        y_0 += WIDGET_HEIGHT + VERTICAL_GAP

    return tab_widget


def main():
    """Uses dictionary of PVs to create widgets and then ouput the CS-Studio and Phoebus files"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "LS1FS1 Virtual Accelerator")

    # Creates the tab container to hold all the various monitors
    tab_container = create_tab_container(screen)

    pv_data = data_reading()

    # Creates a tab for each type of monitor
    for device_type in get_device_types(pv_data):
        tab_container.add_tab(device_type, create_tab_widget(pv_data, device_type))

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
