""" Creates the graph tab for the VA OPI """

from opigen import Renderer, widgets
from opigen.contrib import Display

from time_travel_control import Colors

# Variables to control widget positioning
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

HORIZONTAL_GAP = 5
VERTICAL_GAP = 5

GRAPH_WIDTH = SCREEN_WIDTH - 100
GRAPH_HEIGHT = SCREEN_HEIGHT - 100
GRAPH_LINE_WIDTH = 5


def create_graphs_tab(folder_path):
    """Creates the OPI for the XY Graphs with BPM data"""
    # OPI to render to
    opi = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "Graphs")
    opi.add_scale_options()

    # Creates the graph and sets x axis title
    graph = widgets.XYGraph(HORIZONTAL_GAP, VERTICAL_GAP, GRAPH_WIDTH, GRAPH_HEIGHT)
    graph.set_axis_title("Position of Device (m)", 0)
    graph.set_axis_grid(False, 0)
    graph.set_axis_scale(0, 160, 0)

    # Adding traces for x and y readbacks
    graph.add_trace("VA:LS1FS1:BPM_ALL:X_RD",
                    "VA:LS1FS1:BPM_ALL:POS_RD",
                    legend="X_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    trace_color=Colors.RED)

    graph.add_trace("VA:LS1FS1:BPM_ALL:Y_RD",
                    "VA:LS1FS1:BPM_ALL:POS_RD",
                    legend="Y_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    trace_color=Colors.BLUE)

    # Setting y axis for pos readbacks
    graph.set_axis_title("Value Reading (m)", 1)
    graph.set_axis_grid(False, 1)
    graph.set_axis_scale(-0.032, 0.007, 1)
    graph.set_axis_color(Colors.RED, 1)

    # Adding trace for PHA readback
    graph.add_y_axis()
    graph.add_trace("VA:LS1FS1:BPM_ALL:PHA_RD",
                    "VA:LS1FS1:BPM_ALL:POS_RD",
                    legend="PHA_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    y_axis=1,
                    trace_color=Colors.YELLOW)

    # Setting y axis for PHA readbacks
    graph.set_axis_title("Value Reading (degrees)", 2)
    graph.set_axis_grid(False, 2)
    graph.set_axis_scale(-600, 600, 2)
    graph.set_axis_color(Colors.YELLOW, 2)

    # Adding trace for ENG readback
    graph.add_y_axis()
    graph.add_trace("VA:LS1FS1:BPM_ALL:ENG_RD",
                    "VA:LS1FS1:BPM_ALL:POS_RD",
                    legend="ENG_RD",
                    line_width=GRAPH_LINE_WIDTH,
                    y_axis=2,
                    trace_color=Colors.GREEN)

    # Setting y axis for ENG readbacks
    graph.set_axis_title("Value Reading (MeV)", 3)
    graph.set_axis_grid(False, 3)
    graph.set_axis_scale(-1, 60, 3)
    graph.set_axis_color(Colors.GREEN, 3)

    opi.add_child(graph)

    opi_renderer = Renderer(opi)
    opi_renderer.to_opi(f"{folder_path}{'Graphs'}_tab.opi")
    opi_renderer.to_bob(f"{folder_path}{'Graphs'}_tab.bob")
