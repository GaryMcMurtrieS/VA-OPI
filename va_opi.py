""" Creates Phoebus and CS-Studio OPI Files for reading Accelerator Data"""

import pandas as pd
from opigen import Renderer, widgets
from opigen.contrib import Display, TextEntry, TextUpdate

# Variables to control widget positioning
FILENAME = "va_opi"
WIDGET_HEIGHT = 25
NAME_WIDTH = 160
DATA_WIDTH = 700
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5


def create_tab_container(screen):
    """Creates and adds tab container to the screen"""
    tab_container = widgets.TabbedContainer(HORIZONTAL_GAP, VERTICAL_GAP,
                                            NAME_WIDTH + DATA_WIDTH + (3 * HORIZONTAL_GAP) + 12,
                                            SCREEN_HEIGHT + 33)
    screen.add_child(tab_container)
    return tab_container


def get_device_types(pv_data):
    """Gets all the device types and sorts them"""
    device_types = pv_data["Device Type"].unique()
    device_types.sort()
    return device_types


def create_columns_and_get_width(filtered_pvs, tab_widget):
    """Creates column labels for the given tab"""
    # Gets and sorts all column names
    column_names = sorted(filtered_pvs["Variable Identifier"].unique())
    column_count = len(column_names)
    column_width = (DATA_WIDTH / column_count) - HORIZONTAL_GAP

    # Creates all the widgets for column name labels
    x_0 = HORIZONTAL_GAP + NAME_WIDTH + HORIZONTAL_GAP

    for column_name in column_names:
        column_label = widgets.Label(x_0, HORIZONTAL_GAP, column_width, WIDGET_HEIGHT, column_name)
        tab_widget.add_child(column_label)
        x_0 += column_width + HORIZONTAL_GAP

    return column_width, column_names


def create_tab_widget(filtered_pvs, device_type):
    """Creates the container that goes into a given tab"""
    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0,
                                           NAME_WIDTH + DATA_WIDTH + (3 * HORIZONTAL_GAP) + 10,
                                           SCREEN_HEIGHT, device_type)

    # Create column labels
    column_width, column_names = create_columns_and_get_width(filtered_pvs, tab_widget)

    # Get all the devices names with that type
    device_names = sorted((filtered_pvs["System Identifier"] + ':' + filtered_pvs["Location"] +
                           '_' + filtered_pvs["Managing Device"] + ':' +
                           filtered_pvs["Device Type"] + '_' + filtered_pvs["Position"]).unique())

    # Once we have all the device names, we loop through and add a row for each of them
    y_0 = VERTICAL_GAP + WIDGET_HEIGHT + VERTICAL_GAP
    for device in device_names:
        # Label for the devices name
        device_label = widgets.Label(HORIZONTAL_GAP, y_0, NAME_WIDTH, WIDGET_HEIGHT, device)
        tab_widget.add_child(device_label)

        x_0 = HORIZONTAL_GAP + NAME_WIDTH + HORIZONTAL_GAP

        # Next, each of that devices parameters is added as a widget
        # CSET parameters can take text input and be changed, everything else cannot be changed
        # and only read back
        for parameter in column_names:
            process_variable = device + ':' + parameter
            parameter_output = (TextEntry if parameter.endswith("CSET") else TextUpdate)(
                x_0, y_0, column_width, WIDGET_HEIGHT, process_variable)
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

    # Reads in the data with all the pvs to be displayed
    pv_data = pd.read_csv("va_pvs.csv").dropna()

    # Creates a tab for each type of monitor
    for device_type in get_device_types(pv_data):
        # Filters data to only data on that tab
        filtered_pvs = pv_data[pv_data["Device Type"] == device_type]
        # Creates, fills, and adds the tab to the tab container
        tab_container.add_tab(device_type, create_tab_widget(filtered_pvs, device_type))

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
