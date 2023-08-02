"""Creates the time-travel controls for a given tab."""

from opigen import widgets
from opigen.opimodel import fonts, rules
from opigen.opimodel.colors import Color
from opigen.opimodel.scripts import Script

# Variables to control widget positioning
HORIZONTAL_GAP = 5
VERTICAL_GAP = 5

WIDGET_HEIGHT = 30
BUTTON_WIDTH = 200

GRAPH_LINE_WIDTH = 5

TIME_ENTRY_WIDTH = 280

COLOR_ALPHA = 128


class Colors:
    """Enumerator for graph colors"""
    BLACK = Color((0, 0, 0))
    BLUE = Color((66, 133, 244), alpha=COLOR_ALPHA)
    DARK_BLUE = Color((3, 37, 126))
    GREEN = Color((69, 168, 83), alpha=COLOR_ALPHA)
    RED = Color((234, 67, 53), alpha=COLOR_ALPHA)
    YELLOW = Color((251, 188, 5), alpha=COLOR_ALPHA)


def create_time_travel_control_row(parent_widget, device_type, filtered_pvs, y_0):
    """Creates the control row for the time travel mode"""
    x_0 = HORIZONTAL_GAP

    # Time Travel Toggle button, toggles between time travel mode and current data
    time_travel_toggle = widgets.ToggleButton(x_0, y_0, BUTTON_WIDTH, WIDGET_HEIGHT,
                                              "Time Travel On", "Time Travel Off",
                                              f"loc://$(DID)_time_travel_{device_type}(0)")
    time_travel_toggle.set_font(fonts.DEFAULT_BOLD)
    parent_widget.add_child(time_travel_toggle)

    x_0 += BUTTON_WIDTH + HORIZONTAL_GAP

    # Default timestamp that will be used for archive data retrieval
    default_time = "2023-07-07T15:00:00.00-04:00"

    # LED that shows if timestamp matches timestamp of pulled data
    timestamp_led = widgets.Led(x_0, y_0, WIDGET_HEIGHT, WIDGET_HEIGHT,
                                f"loc://time_led_{device_type}(0)")

    # Rule, sets LED to be off when time travel is off
    timestamp_led.add_rule(
        rules.SelectionRule("pv_name", f"loc://$(DID)_time_travel_{device_type}(0)",
                            "Time Travel Toggle Rule", [(0, "sim://const(0)"),
                                                        (1, f"loc://time_led_{device_type}(0)")]))

    # Script that controls whether LED is on or off
    timestamp_led_script = Script("scripts/timestamp_led_script.py")
    timestamp_led_script.add_pv(f"loc://time_led_{device_type}(0)", False)
    timestamp_led_script.add_pv(f'loc://time_{device_type}("{default_time}")', True)
    timestamp_led_script.add_pv(f"loc://$(DID)_trigger_{device_type}(0)", True)
    timestamp_led_script.add_pv(f'loc://internal_state_{device_type}("{default_time}")', False)
    timestamp_led_script.add_pv(f"loc://$(DID)_time_travel_{device_type}(0)", False)
    timestamp_led_script.add_pv(f'loc://debug_message_{device_type}', False)

    timestamp_led.add_script(timestamp_led_script)
    parent_widget.add_child(timestamp_led)

    x_0 += WIDGET_HEIGHT + HORIZONTAL_GAP

    # Time entry box, used to choose when to pull data from
    timestamp_entry = widgets.TextEntry(x_0, y_0, TIME_ENTRY_WIDTH, WIDGET_HEIGHT,
                                        f'loc://time_{device_type}("{default_time}")')
    timestamp_entry.set_font(fonts.DEFAULT)
    parent_widget.add_child(timestamp_entry)

    x_0 += TIME_ENTRY_WIDTH + HORIZONTAL_GAP

    # Action button that pulls historic data and displays it
    pull_button = widgets.ActionButton(x_0, y_0, BUTTON_WIDTH, WIDGET_HEIGHT, "Pull Data")
    pull_button.set_font(fonts.DEFAULT_BOLD)
    pull_button.add_write_pv(f"loc://$(DID)_trigger_{device_type}(0)", 1)

    # Script that actually runs the command to pull the data
    pull_script = Script("scripts/pull_data_script.py")

    # Trigger PV that runs the script
    pull_script.add_pv(f"loc://$(DID)_trigger_{device_type}(0)", True)

    # PV that controls when to pull archival data from
    pull_script.add_pv(f'loc://time_{device_type}("{default_time}")', False)
    pull_script.add_pv(f"loc://$(DID)_time_travel_{device_type}(0)", False)
    pull_script.add_pv(f'loc://debug_message_{device_type}', False)

    # Creates list of PVs that will have their archived data pulled
    pvs = list(filtered_pvs["System Identifier"] + ':' + filtered_pvs["Location"] + '_' +
               filtered_pvs["Managing Device"] + ':' + filtered_pvs["Device Type"] + '_' +
               filtered_pvs["Position"] + ':' + filtered_pvs["Variable Identifier"])

    # Adds each of the pvs to the script
    for process_variable in pvs:
        pull_script.add_pv(process_variable, False)
        pull_script.add_pv(f'loc://time_travel_{process_variable}("No Data Yet")', False)

    pull_button.add_script(pull_script)
    parent_widget.add_child(pull_button)

    x_0 += BUTTON_WIDTH + HORIZONTAL_GAP

    # Action button that sets current values to historic data
    set_button = widgets.ActionButton(x_0, y_0, BUTTON_WIDTH, WIDGET_HEIGHT, "Set Data")
    set_button.set_font(fonts.DEFAULT_BOLD)

    set_script = Script("scripts/set_data_script.py")

    set_button.add_script(set_script)
    parent_widget.add_child(set_button)

    y_0 += WIDGET_HEIGHT + VERTICAL_GAP
    x_0 = HORIZONTAL_GAP

    debug_width = (3 * BUTTON_WIDTH) + (4 * HORIZONTAL_GAP) + WIDGET_HEIGHT + TIME_ENTRY_WIDTH
    debug_display = widgets.TextEntry(
        x_0, y_0, debug_width, WIDGET_HEIGHT,
        f'loc://debug_message_{device_type}("Initialization Complete.")')
    debug_display.horizontal_alignment = widgets.HAlign.LEFT
    debug_display.set_font(fonts.DEFAULT)
    parent_widget.add_child(debug_display)

    return y_0 + WIDGET_HEIGHT + VERTICAL_GAP
