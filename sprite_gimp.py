#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import math
from gimpfu import *
import sprite_vgen

def python_icysprites(timg, tdrawable, outfile):
    sprites = []
    for i in range(0, len(timg.layers) - 1):
        L = timg.layers[i]
        x, y = L.offsets
        width = L.width
        height = L.height
        data = []
        rgn = L.get_pixel_rgn(0, 0, width, height)
        for ly in range(height):
            line = []
            for lx in range(width):
                p = rgn[lx, ly]
                pix = 0
                # Convert RGB/RGBA to 2bpp
                r = ord(p[0])
                g = ord(p[1])
                b = ord(p[2])
                a = 255
                if len(p) > 3:
                    a = ord(p[3])
                if a < 128 or (r == g and g == b):
                    pix = 0
                elif(r > g) and (r > b):
                    pix = 1
                elif(g > r) and (g > b):
                    pix = 2
                elif(b > r) and (b > g):
                    pix = 3
                else:
                    pix = 0
                line.append(pix)
            data.append(line)
        sprites.append((x, y, width, height, data))
    sprite_vgen.write_vlog(sprites, outfile)
register(
        "python_fu_icysprites",
        "Generate a Verilog sprite renderer based on layers in the image",
        "Generate a Verilog sprite renderer based on layers in the image",
        "David Shah",
        "David Shah",
        "2018",
        "<Image>/Filters/Animation/_IcySprites...",
        "RGB, RGB*",
        [
                (PF_FILE, "outfile", "Output File", "spritegen.v")
        ],
        [],
        python_icysprites)

main()
