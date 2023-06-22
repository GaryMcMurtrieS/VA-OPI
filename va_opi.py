""" Creates the top level OPI for the Virtual Accelerator """

from opigen import Renderer, widgets
from opigen.contrib import Display

import va_opi_tabs

# Variables to control widget positioning
FILENAME = "va_opi"
TAB_FOLDER = "va_opi_tabs/"

SCREEN_WIDTH = va_opi_tabs.SCREEN_WIDTH
SCREEN_HEIGHT = va_opi_tabs.SCREEN_HEIGHT

HORIZONTAL_GAP = va_opi_tabs.HORIZONTAL_GAP
VERTICAL_GAP = va_opi_tabs.VERTICAL_GAP

EMBED_WIDTH = SCREEN_WIDTH - HORIZONTAL_GAP * 2 - 2
EMBED_HEIGHT = SCREEN_HEIGHT - VERTICAL_GAP * 2 - 33


def main():
    """Creates the tab container that holds all the embedded containers as tabs"""
    # Sets up screen
    screen = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "LS1FS1 Virtual Accelerator")

    # Creates the tab container to hold all the various monitors
    tab_container = widgets.TabbedContainer(HORIZONTAL_GAP, VERTICAL_GAP,
                                            SCREEN_WIDTH - HORIZONTAL_GAP * 2,
                                            SCREEN_HEIGHT - VERTICAL_GAP * 2)
    screen.add_child(tab_container)

    # Create all the OPIs for the embedded containers
    device_types = va_opi_tabs.create_embeds()

    # Creates the first two tabs, one for SVR and one for the XY Graphs
    tab_container.add_tab(
        "SVR",
        widgets.EmbeddedContainer(0, 0, EMBED_WIDTH, EMBED_HEIGHT, f"{TAB_FOLDER}{'SVR'}_tabs.opi"))
    tab_container.add_tab(
        "Graphs",
        widgets.EmbeddedContainer(0, 0, EMBED_WIDTH, EMBED_HEIGHT,
                                  f"{TAB_FOLDER}{'Graphs'}_tabs.opi"))

    # Creates a tab for each type of monitor
    for device_type in device_types:
        tab_widget = widgets.EmbeddedContainer(0, 0, EMBED_WIDTH, EMBED_HEIGHT,
                                               f"{TAB_FOLDER}{device_type}_tabs.opi")

        tab_widget.resize_behaviour = widgets.ResizeBehaviour.SCROLL
        tab_container.add_tab(device_type, tab_widget)

    # Outputs to file
    screen_renderer = Renderer(screen)
    screen_renderer.to_opi(f"{FILENAME}.opi")
    screen_renderer.to_bob(f"{FILENAME}.bob")


if __name__ == "__main__":
    main()
