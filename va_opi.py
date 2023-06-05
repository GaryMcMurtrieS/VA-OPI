#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opigen import widgets
from opigen.contrib import TextUpdate
from opigen.contrib import Display
from opigen import Renderer

data = [
    ('LS1_CA01:BPM_D1129', 'VA:LS1_CA01:BPM_D1129:X_RD', 'VA:LS1_CA01:BPM_D1129:Y_RD'),
    ('LS1_CA01:BPM_D1144', 'VA:LS1_CA01:BPM_D1144:X_RD', 'VA:LS1_CA01:BPM_D1144:Y_RD')
]

height = 25 # Controls how tall boxes are
hgap, vgap = 5, 25 # Separation between boxes
w_name, w_xpos, w_ypos = [200, 60, 60]

# name column
x_name, y0 = 5, 5
# xpos column
x_xpos = x_name + w_name + hgap
# ypos column
x_ypos = x_xpos + w_xpos + hgap

# screen
screen = Display(800, 600, "BPM Readings")

for name, xpv, ypv in data:
    # label
    name_lbl = widgets.Label(x_name, y0, w_name, height, name)
    x_rd_text = TextUpdate(x_xpos, y0, w_xpos, height, xpv)
    y_rd_text = TextUpdate(x_ypos, y0, w_ypos, height, ypv)
    screen.add_child(name_lbl)
    screen.add_child(x_rd_text)
    screen.add_child(y_rd_text)
    y0 += height + vgap

#
filename = "va_opi"
r = Renderer(screen)
r.to_opi(F"{filename}.opi")
r.to_bob(F"{filename}.bob")
