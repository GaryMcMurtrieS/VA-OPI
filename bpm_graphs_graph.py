""" Generates XY Graphs to display BPM"""

import pandas as pd
from opigen import Renderer, widgets
from opigen.contrib import Display, TextEntry, TextUpdate

# Variables to control widget positioning
FILENAME = "bpm_opi_graph"
WIDGET_HEIGHT = 25
TOTAL_WIDTH = 850
NAME_WIDTH = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5


def create_graph(bpm_data, screen):
    """Creates the container that goes into a given tab"""
    graph = widgets.XYGraph(5, 5, 1000, 500)

    for _, device in bpm_data.iterrows():
        process_variable = device["System Identifier"] + ':' + device["Location"] + '_' + device[
            "Managing Device"] + ':' + device["Device Type"] + '_' + device["Position"] + ":X_RD"
        graph.add_trace(f"sim://const({device['Position'][1:]})", process_variable)

    position_info = sorted([i[1:] for i in bpm_data["Position"]])

    graph.set_axis_scale(-0.01, 0.01, False)
    graph.set_axis_scale(position_info[0], position_info[-1])
    screen.add_child(graph)


def main():
    """Uses dictionary of PVs to create widgets and then output the CS-Studio and Phoebus files"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "BPM Readings")

    # Reads in the data with all the pvs to be displayed
    pv_data = pd.read_csv("va_pvs.csv")
    xrd_data = pv_data[pv_data["Variable Identifier"] == "X_RD"]

    create_graph(xrd_data, screen)

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
