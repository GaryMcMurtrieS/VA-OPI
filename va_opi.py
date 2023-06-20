""" Creates Phoebus and CS-Studio OPI Files for reading Accelerator Data """

import pandas as pd
from opigen import Renderer, widgets
from opigen.contrib import Display, TextEntry, TextUpdate

# Variables to control widget positioning
FILENAME = "va_opi"
WIDGET_HEIGHT = 25
TOTAL_WIDTH = 850
NAME_WIDTH = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 500
GRAPH_LINE_WIDTH = 5


def create_columns_and_get_width(filtered_pvs, tab_widget):
    """Creates column labels for the given tab"""
    # Gets and sorts all column names
    column_names = sorted(filtered_pvs["Variable Identifier"].unique())
    column_count = len(column_names)
    column_width = ((TOTAL_WIDTH - NAME_WIDTH) / column_count) - HORIZONTAL_GAP

    # Creates all the widgets for column name labels
    x_0 = HORIZONTAL_GAP + NAME_WIDTH + HORIZONTAL_GAP

    for column_name in column_names:
        column_label = widgets.Label(x_0, VERTICAL_GAP, column_width, WIDGET_HEIGHT, column_name)
        tab_widget.add_child(column_label)

        x_0 += column_width + HORIZONTAL_GAP

    return column_width, column_names


def create_widget_row(tab_widget, device, column_names, column_width, y_0):
    """Creates a row of widgets for a given device"""
    # Label for the devices name
    device_label = widgets.Label(HORIZONTAL_GAP, y_0, NAME_WIDTH, WIDGET_HEIGHT, device[3:])
    tab_widget.add_child(device_label)

    x_0 = HORIZONTAL_GAP + NAME_WIDTH + HORIZONTAL_GAP

    # Next, each of that devices parameters is added as a widget
    # CSET parameters can take text input and be changed, everything else cannot be changed
    # and only read back
    for parameter in column_names:
        process_variable = device + ':' + parameter
        parameter_output = (TextEntry if parameter.endswith("CSET") or device.endswith("SVR") else
                            TextUpdate)(x_0, y_0, column_width, WIDGET_HEIGHT, process_variable)
        tab_widget.add_child(parameter_output)

        x_0 += column_width + HORIZONTAL_GAP


def create_svr_tab(svr_data):
    """Creates the tab for SVR data, which is different because of how the data is stored."""
    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10,
                                           SCREEN_HEIGHT, "SVR")

    # Create column labels
    column_width, column_names = create_columns_and_get_width(svr_data, tab_widget)

    # Once we have all the device names, we loop through and add a row for each of them
    create_widget_row(tab_widget, "VA:SVR", column_names, column_width,
                      VERTICAL_GAP + WIDGET_HEIGHT + VERTICAL_GAP)

    return tab_widget


def create_graphs_tab():
    """Creates a tab for the XY Graphs with BPM data"""
    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10,
                                           SCREEN_HEIGHT, "Graphs")

    # Creates the graph and sets x axis title
    graph = widgets.XYGraph(HORIZONTAL_GAP, VERTICAL_GAP, GRAPH_WIDTH, GRAPH_HEIGHT)
    graph.set_axis_title("Position of Device (m)", 0)

    # Adding traces for x and y readbacks
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:X_RD",
                    legend="X_RD",
                    line_width=GRAPH_LINE_WIDTH)
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:Y_RD",
                    legend="Y_RD",
                    line_width=GRAPH_LINE_WIDTH)

    # Setting y axis for pos readbacks
    graph.set_axis_title("Value Reading (m)", 1)
    y_limit = 0.01
    graph.set_axis_scale(-y_limit, y_limit, 1)

    # Adding trace for PHA readback
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:PHA_RD",
                    legend="PHA_RD",
                    line_width=GRAPH_LINE_WIDTH)

    graph.add_axis(1)
    graph.change_trace_axis(2, 1, 2)

    # Setting y axis for PHA readbacks
    graph.set_axis_title("Value Reading (degrees)", 2)
    y_limit = 300
    graph.set_axis_scale(-y_limit, y_limit, 2)

    # Adding trace for ENG readback
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:ENG_RD",
                    legend="ENG_RD",
                    line_width=GRAPH_LINE_WIDTH)

    graph.add_axis(1)
    graph.change_trace_axis(3, 1, 3)

    # Setting y axis for ENG readbacks
    graph.set_axis_title("Value Reading (MeV)", 3)
    y_limit = 30
    graph.set_axis_scale(-y_limit, y_limit, 3)

    tab_widget.add_child(graph)

    return tab_widget


def create_tab_widget(filtered_pvs, device_type):
    """Creates the container that goes into a given tab"""
    # Creates a singular widget to add to the tab that contains all other widgets
    tab_widget = widgets.GroupingContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10,
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
        create_widget_row(tab_widget, device, column_names, column_width, y_0)

        y_0 += WIDGET_HEIGHT + VERTICAL_GAP

    return tab_widget


def main():
    """Uses dictionary of PVs to create widgets and then output the CS-Studio and Phoebus files"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "LS1FS1 Virtual Accelerator")

    # Creates the tab container to hold all the various monitors
    tab_container = widgets.TabbedContainer(HORIZONTAL_GAP, VERTICAL_GAP,
                                            TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 12,
                                            SCREEN_HEIGHT + 33)
    screen.add_child(tab_container)

    # Reads in the data with all the pvs to be displayed
    pv_data = pd.read_csv("va_pvs.csv")
    svr_data = pv_data[pv_data["Location"] == "SVR"]
    pv_data = pv_data.dropna()

    # Creates the first two tabs, one for SVR and one for the XY Graphs
    tab_container.add_tab("SVR", create_svr_tab(svr_data))
    tab_container.add_tab("Graphs", create_graphs_tab())

    # Creates a tab for each type of monitor
    for device_type in sorted(pv_data["Device Type"].unique()):
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
