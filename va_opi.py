from opigen import Renderer
from opigen import widgets
from opigen.contrib import Display
from opigen.contrib import TextUpdate

# Variables to control widget positioning
filename = "va_opi"
box_height = 25  # Controls how tall boxes are
horizontal_gap = 5
vertical_gap = 5 # Separation between boxes

name_width = 180
text_width = 100

# Name column
name_x = 5
y0 = 5

# xpos column
x_xpos = name_x + name_width + horizontal_gap
# ypos column
x_ypos = x_xpos + text_width + horizontal_gap

# Reads in data from file
va_pvs = open("VA_pvlist.txt", "r")
raw_data = va_pvs.readlines()

data = {}
for line in raw_data:
    line = line.rstrip()
    name = ":".join(line.split(":")[1:3])

    if name not in data:
        data[name] = []

    data[name].append(line)

# Sets up screen
screen = Display(800, 600, "BPM Readings")

for key in data.keys():
    name_lbl = widgets.Label(name_x, y0, name_width, box_height, key)
    screen.add_child(name_lbl)

    x0 = name_x + name_width + horizontal_gap

    for child in data[key]:
        child_text = TextUpdate(x0, y0, text_width, box_height, child)
        screen.add_child(child_text)
        x0 += text_width + horizontal_gap

    y0 += box_height + vertical_gap

# for name, xpos, ypos in data:
#     name_lbl = widgets.Label(x_name, y0, w_name, box_height, name)
#     x_rd_text = TextUpdate(x_xpos, y0, w_xpos, box_height, xpos)
#     y_rd_text = TextUpdate(x_ypos, y0, w_ypos, box_height, ypos)
#     screen.add_child(name_lbl)
#     screen.add_child(x_rd_text)
#     screen.add_child(y_rd_text)
#     y0 += box_height + gap_v

# Outputs to file
r = Renderer(screen)
r.to_opi(f"{filename}.opi")
r.to_bob(f"{filename}.bob")
