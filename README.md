# IcySprites

IcySprites is the easiest way to use a graphical TFT with an FPGA. It does this
by emulating an old-fashioned segment LCD, with input lines controlling each
"segment".

Currently it is in proof-of-concept. It is implemented as a GIMP plugin. Each
layer, except the background, corresponds to a single segment "sprite". Running
the plugin generates a Verilog module that contains the video generator. At the
moment LCD timing generation is not contained in the generated Verilog, and
must be connected seperately.
