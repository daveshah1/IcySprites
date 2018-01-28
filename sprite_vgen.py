#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import math


import os

# Constant parameters, that shouldn't really be constant
x_pos_width = 12
y_pos_width = 12
pixel_width = 2

# Round a value to the next highest power of two - this is used to optimise the
# HDL implementation
def next_pow2(x):
    p = 1
    while(p < x):
        p *= 2
    return p


# Given a list of sprites in the format (x, y, width, height, data); generate the
# corresponding verilog and BRAM initialisation data

def write_vlog(sprites, filename):
    with open(filename, 'w') as vf:
        N = len(sprites)
        print("module sprites(", file=vf)
        print("\tinput clock, reset,", file=vf)
        print("\tinput [%d:0] vx," % (x_pos_width - 1), file=vf)
        print("\tinput [%d:0] vy," % (y_pos_width - 1), file=vf)
        print("\tinput [%d:0] enables," % (N - 1), file=vf)
        print("\toutput reg [%d:0] pixel);" % (pixel_width - 1), file=vf)

        romoffsets = []
        current_offset = 0
        for i in range(N):
            (x, y, width, height, data) = sprites[i]
            romoffsets.append(current_offset)
            current_offset += next_pow2(width) * next_pow2(height)

        romsize = current_offset
        awidth = math.ceil(math.log(romsize, 2))

        print("reg active = 1'b0;", file=vf)
        print("reg [%d:0] romaddr = 0;" % (awidth - 1), file=vf)
        print("", file=vf)
        print("// Sprite position lookup", file=vf)
        print("always @(posedge clock) begin", file=vf)
        print("\tif(reset) begin", file=vf)
        print("\t\tactive <= 1'b0;", file=vf)
        print("\t\tromaddr <= 1'b0;", file=vf)
        print("\tend else begin", file=vf)
        for i in xrange(N-1, 0, -1):
            (x, y, width, height, data) = sprites[i]
            c_else = " else " if i < (N-1) else ""
            print("\t\t%sif(enables[%d] && (vx >= %d) && (vx < %d) && (vy >= %d) && (vy < %d)) begin" %
                  (c_else, i, x, (x + width), y, (y+width)), file=vf)
            print("\t\t\tactive <= 1'b1;", file=vf)
            print("\t\t\tromaddr <= %d + ((vy - %d) * %d) + (vx - %d);" % (romoffsets[i], y, next_pow2(width), x), file=vf)
            print("\t\tend", file=vf)
        print("\t\telse begin", file=vf)
        print("\t\t\tactive <= 1'b0;", file=vf)
        print("\t\tend", file=vf)
        print("\tend", file=vf)
        print("end", file=vf)
        print("", file=vf)
        print("// Sprite data ROM", file=vf)
        romfilename = filename.replace(".v", "") + "_srom.dat"
        print("reg [%d:0] srom[0:%d];" % (pixel_width - 1, romsize - 1), file=vf)
        print("initial $readmemh(\"%s\", srom);" % (os.path.basename(romfilename)), file=vf)
        print("", file=vf)
        print("reg [%d:0] srom_dat;" % (pixel_width - 1), file=vf)
        print("reg active_dly;", file=vf)
        print("", file=vf)
        print("always @(posedge clock) begin", file=vf)
        print("\tsrom_dat <= srom[romaddr];", file=vf)
        print("\tactive_dly <= active;", file=vf)
        print("\tpixel <= active_dly ? srom_dat : 0;", file=vf)
        print("end", file=vf)

        print("endmodule", file=vf);
        with open(romfilename, 'w') as rf:
            for i in range(N):
                (x, y, width, height, data) = sprites[i]
                for ry in range(next_pow2(height)):
                    for rx in range(next_pow2(width)):
                        pix = 0
                        if (ry < height) and (rx < width):
                            pix = data[ry][rx]
                        print("%x" % (pix), file=rf)
