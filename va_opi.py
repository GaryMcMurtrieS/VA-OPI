from opigen import Renderer
from opigen import widgets
from opigen.contrib import Display
from opigen.contrib import TextEntry
from opigen.contrib import TextUpdate

# Variables to control widget positioning
filename = "va_opi"
box_height = 25  # Controls how tall boxes are
horizontal_gap = 5
vertical_gap = 5  # Separation between boxes

name_width = 150
text_width = 600

# Name column
name_x = 5
y0 = 5

# Reads in data from file
va_pvs = open("VA_pvlist.txt", "r")
raw_data = va_pvs.readlines()

data = {}
for line in raw_data:
    line = line.rstrip()

    type = (
        line.split(":")[2].split("_")[0].translate(str.maketrans("", "", "0123456789"))
    )

    if type not in data:
        data[type] = {}

    name = ":".join(line.split(":")[1:3])

    if name not in data[type]:
        data[type][name] = []

    data[type][name].append(line)

# Sets up screen
screen = Display(800, 600, "BPM Readings")

for type in data.keys():
    for key in data[type]:
        name_lbl = widgets.Label(name_x, y0, name_width, box_height, key)
        screen.add_child(name_lbl)

        x0 = name_x + name_width + horizontal_gap

        child_count = len(data[type][key])
        for child in data[type][key]:
            if child[-3:] == "SET":
                child_text = TextEntry(
                    x0, y0, text_width / child_count - horizontal_gap, box_height, child
                )
            else:
                child_text = TextUpdate(
                    x0, y0, text_width / child_count - horizontal_gap, box_height, child
                )

            screen.add_child(child_text)
            x0 += text_width / child_count

        y0 += box_height + vertical_gap

# Outputs to file
r = Renderer(screen)
r.to_opi(f"{filename}.opi")
r.to_bob(f"{filename}.bob")
