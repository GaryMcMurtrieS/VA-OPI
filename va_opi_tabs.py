""" For each tab in the VA OPI, creates an OPI that is embedded into that tab """

import pandas as pd
from opigen import Renderer, widgets
from opigen.contrib import Display, TextEntry, TextUpdate
from opigen.opimodel.colors import Color

# Variables to control widget positioning
FILENAME = "va_opi"
TAB_FOLDER_PATH = "va_opi_tabs/"

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

HORIZONTAL_GAP = 5
VERTICAL_GAP = 5

WIDGET_HEIGHT = 25
TOTAL_WIDTH = SCREEN_WIDTH - HORIZONTAL_GAP * 2 - 25
NAME_WIDTH = 150

GRAPH_WIDTH = SCREEN_WIDTH - 100
GRAPH_HEIGHT = SCREEN_HEIGHT - 100
GRAPH_LINE_WIDTH = 5

COLOR_ALPHA = 128


class Colors:
    """Enumerator for graph colors"""
    RED = Color((234, 67, 53), alpha=COLOR_ALPHA)
    BLUE = Color((66, 133, 244), alpha=COLOR_ALPHA)
    YELLOW = Color((251, 188, 5), alpha=COLOR_ALPHA)
    GREEN = Color((69, 168, 83), alpha=COLOR_ALPHA)


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
        column_label.horizontal_alignment = widgets.HAlign.RIGHT
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
        parameter_output.horizontal_alignment = widgets.HAlign.RIGHT
        tab_widget.add_child(parameter_output)

        x_0 += column_width + HORIZONTAL_GAP


def create_svr_tab(folder_path, svr_data):
    """Creates the OPI for SVR data, which is different because of how the data is stored."""
    # OPI to render to
    opi = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "SVR")

    # Create column labels
    column_width, column_names = create_columns_and_get_width(svr_data, opi)

    # Once we have all the device names, we loop through and add a row for each of them
    create_widget_row(opi, "VA:SVR", column_names, column_width,
                      VERTICAL_GAP + WIDGET_HEIGHT + VERTICAL_GAP)

    # Outputs to file
    opi_renderer = Renderer(opi)
    opi_renderer.to_opi(f"{folder_path}{'SVR'}_tab.opi")
    opi_renderer.to_bob(f"{folder_path}{'SVR'}_tab.bob")


def create_graphs_tab(folder_path):
    """Creates the OPI for the XY Graphs with BPM data"""
    # OPI to render to
    opi = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "Graphs")

    # Creates the graph and sets x axis title
    graph = widgets.XYGraph(HORIZONTAL_GAP, VERTICAL_GAP, GRAPH_WIDTH, GRAPH_HEIGHT)
    graph.set_axis_title("Position of Device (m)", 0)
    graph.set_axis_scale(0, 160, 0)

    # Adding traces for x and y readbacks
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:X_RD",
                    legend="X_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    trace_color=Colors.RED)

    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:Y_RD",
                    legend="Y_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    trace_color=Colors.BLUE)

    # Setting y axis for pos readbacks
    graph.set_axis_title("Value Reading (m)", 1)
    graph.set_axis_scale(-0.032, 0.007, 1)
    graph.set_axis_color(Colors.RED, 1)

    # Adding trace for PHA readback
    graph.add_y_axis()
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:PHA_RD",
                    legend="PHA_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    y_axis=2,
                    trace_color=Colors.YELLOW)

    # Setting y axis for PHA readbacks
    graph.set_axis_title("Value Reading (degrees)", 2)
    graph.set_axis_scale(-600, 600, 2)
    graph.set_axis_color(Colors.YELLOW, 2)

    # Adding trace for ENG readback
    graph.add_y_axis()
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:ENG_RD",
                    legend="ENG_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    y_axis=3,
                    trace_color=Colors.GREEN)

    # Setting y axis for ENG readbacks
    graph.set_axis_title("Value Reading (MeV)", 3)
    graph.set_axis_scale(-1, 60, 3)
    graph.set_axis_color(Colors.GREEN, 3)

    opi.add_child(graph)

    opi_renderer = Renderer(opi)
    opi_renderer.to_opi(f"{folder_path}{'Graphs'}_tab.opi")
    opi_renderer.to_bob(f"{folder_path}{'Graphs'}_tab.bob")


def create_tab_widget(folder_path, filtered_pvs, device_type):
    """Creates the OPI that goes into a given tab"""
    # OPI to render to
    opi = Display(SCREEN_WIDTH, SCREEN_HEIGHT, device_type)

    # Create column labels
    column_width, column_names = create_columns_and_get_width(filtered_pvs, opi)

    # Get all the devices names with that type
    device_names = sorted((filtered_pvs["System Identifier"] + ':' + filtered_pvs["Location"] +
                           '_' + filtered_pvs["Managing Device"] + ':' +
                           filtered_pvs["Device Type"] + '_' + filtered_pvs["Position"]).unique())

    # Once we have all the device names, we loop through and add a row for each of them
    y_0 = VERTICAL_GAP + WIDGET_HEIGHT + VERTICAL_GAP

    for device in device_names:
        create_widget_row(opi, device, column_names, column_width, y_0)
        y_0 += WIDGET_HEIGHT + VERTICAL_GAP

    # Outputs to file
    opi_renderer = Renderer(opi)
    opi_renderer.to_opi(f"{folder_path}{device_type}_tab.opi")
    opi_renderer.to_bob(f"{folder_path}{device_type}_tab.bob")


def create_embeds(folder_path=TAB_FOLDER_PATH):
    """Creates all the embedded OPIs and returns list of device types for tab creation"""
    # Reads in the data with all the pvs to be displayed
    pv_data = pd.read_csv("va_pvs.csv")
    svr_data = pv_data[pv_data["Location"] == "SVR"]
    pv_data = pv_data.dropna()

    # Creates the first two OPIs, one for SVR and one for the XY Graphs
    create_svr_tab(folder_path, svr_data)
    create_graphs_tab(folder_path)

    # Creates an OPI for each type of device
    device_types = sorted(pv_data["Device Type"].unique())
    for device_type in device_types:
        # Filters data to only data on that tab
        filtered_pvs = pv_data[pv_data["Device Type"] == device_type]
        # Creates, fills, and outputs the OPI for that device type
        create_tab_widget(folder_path, filtered_pvs, device_type)

    # Returns Device types to know what tabs need to be created
    return device_types


if __name__ == "__main__":
    create_embeds()
