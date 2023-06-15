""" Generates XY Graphs to display BPM"""

from opigen import Renderer, widgets
from opigen.contrib import Display

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
    graph = widgets.XYGraph(VERTICAL_GAP, HORIZONTAL_GAP, GRAPH_WIDTH, GRAPH_HEIGHT)
    graph.add_trace('', "VA:LS1FS1:BPM_ALL:X_RD")
    graph.add_trace('', "VA:LS1FS1:BPM_ALL:Y_RD")
    y_limit = 0.01
    graph.set_axis_scale(-y_limit, y_limit, 1)
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
