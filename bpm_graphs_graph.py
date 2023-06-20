""" Generates XY Graphs to display BPM for testing """

from opigen import Renderer, widgets
from opigen.contrib import Display
from opigen.opimodel.colors import Color

# Variables to control widget positioning
FILENAME = "bpm_opi_graph"
WIDGET_HEIGHT = 25
TOTAL_WIDTH = 850
NAME_WIDTH = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 500


def create_graph():
    """Creates the container that goes into a given tab"""
    # Creates the graph and sets x axis title
    graph = widgets.XYGraph(HORIZONTAL_GAP, VERTICAL_GAP, GRAPH_WIDTH, GRAPH_HEIGHT)
    graph.set_axis_title("Position of Device (m)", 0)

    # Adding traces for x and y readbacks
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:X_RD",
                    legend="X_RD",
                    line_width=5)
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:Y_RD",
                    legend="Y_RD",
                    line_width=5)

    # Setting y axis for pos readbacks
    graph.set_axis_title("Value Reading (m)", 1)
    y_limit = 0.02
    graph.set_axis_scale(-y_limit, y_limit, 1)

    # Adding trace for PHA readback
    graph.add_trace('VA:LS1FS1:BPM_ALL:POS_RD',
                    "VA:LS1FS1:BPM_ALL:PHA_RD",
                    legend="PHA_RD",
                    line_width=5)

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
                    line_width=5)

    graph.add_axis(1)
    graph.change_trace_axis(3, 1, 3)

    # Setting y axis for ENG readbacks
    graph.set_axis_title("Value Reading (MeV)", 3)
    y_limit = 30
    graph.set_axis_scale(-y_limit, y_limit, 3)

    return graph


def main():
    """Uses dictionary of PVs to create widgets and then output the CS-Studio and Phoebus files"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "BPM Readings")
    screen.add_child(create_graph())

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
