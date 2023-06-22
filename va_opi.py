""" Creates Phoebus and CS-Studio OPI Files for reading Accelerator Data """

from opigen import Renderer, widgets
from opigen.contrib import Display

import va_opi_tabs

# Variables to control widget positioning
FILENAME = "va_opi"
TAB_FOLDER = "va_opi_tabs/"

WIDGET_HEIGHT = 25
TOTAL_WIDTH = 850
NAME_WIDTH = 150

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

HORIZONTAL_GAP = 5
VERTICAL_GAP = 5


def main():
    """Uses dictionary of PVs to create widgets and then output the CS-Studio and Phoebus files"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "LS1FS1 Virtual Accelerator")

    # Creates the tab container to hold all the various monitors
    tab_container = widgets.TabbedContainer(HORIZONTAL_GAP, VERTICAL_GAP,
                                            TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 12,
                                            SCREEN_HEIGHT + 33)
    screen.add_child(tab_container)

    device_types = va_opi_tabs.create_embeds()

    # Creates the first two tabs, one for SVR and one for the XY Graphs
    tab_container.add_tab(
        "SVR",
        widgets.EmbeddedContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10, SCREEN_HEIGHT,
                                  f"{TAB_FOLDER}{'SVR'}_tabs.opi"))
    tab_container.add_tab(
        "Graphs",
        widgets.EmbeddedContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10, SCREEN_HEIGHT,
                                  f"{TAB_FOLDER}{'Graphs'}_tabs.opi"))

    # Creates a tab for each type of monitor
    for device_type in device_types:
        tab_widget = widgets.EmbeddedContainer(0, 0, TOTAL_WIDTH + (3 * HORIZONTAL_GAP) + 10,
                                               SCREEN_HEIGHT, f"{TAB_FOLDER}{device_type}_tabs.opi")

        tab_widget.resize_behaviour = widgets.ResizeBehaviour.SCROLL
        tab_container.add_tab(device_type, tab_widget)

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
