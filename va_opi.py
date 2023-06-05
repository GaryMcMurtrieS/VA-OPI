#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opigen import widgets
from opigen.contrib import TextUpdate
from opigen.contrib import Display
from opigen import Renderer

data_sample = [
    ('LS1_CA01:BPM_D1129', 'VA:LS1_CA01:BPM_D1129:X_RD', 'VA:LS1_CA01:BPM_D1129:Y_RD'),
    ('LS1_CA01:BPM_D1144', 'VA:LS1_CA01:BPM_D1144:X_RD', 'VA:LS1_CA01:BPM_D1144:Y_RD')
]

va_pvs = open('VA_pvlist.txt','r')
raw_data = va_pvs.readlines()

data = []
for line in raw_data:
    base = ':'.join(line.split(':')[:3])
    name = base[3:].rstrip()
    x = base + ":X_RD"
    y = base + ":Y_RD"
    data.append((name, x, y))

box_height = 25 # Controls how tall boxes are
gap_h, gap_v = 5, 5 # Separation between boxes
w_name, w_xpos, w_ypos = [200, 60, 60] # Width of sections

# name column
x_name, y0 = 5, 5
# xpos column
x_xpos = x_name + w_name + gap_h
# ypos column
x_ypos = x_xpos + w_xpos + gap_h

# screen
screen = Display(800, 600, "BPM Readings")

for name, xpos, ypos in data:
    # label
    name_lbl = widgets.Label(x_name, y0, w_name, box_height, name)
    x_rd_text = TextUpdate(x_xpos, y0, w_xpos, box_height, xpos)
    y_rd_text = TextUpdate(x_ypos, y0, w_ypos, box_height, ypos)
    screen.add_child(name_lbl)
    screen.add_child(x_rd_text)
    screen.add_child(y_rd_text)
    y0 += box_height + gap_v

#
filename = "va_opi"
r = Renderer(screen)
r.to_opi(F"{filename}.opi")
r.to_bob(F"{filename}.bob")
