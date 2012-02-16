#!/usr/bin/env python

# Adapted straightforwardly from https://github.com/cortesi/scurve/blob/master/testpattern
# Zero little effort has been put into making this pretty, just into getting it to work.

from __future__ import division

import glob
import os.path
import math

import Image, ImageDraw
import scurve
from scurve import progress

def drawmap(map, csource, name, quiet, frame_dir):
    frame_cache = {}

    frame_filename_format = os.path.join(frame_dir, "frame-{frame:07}.png")
    frame_glob = os.path.join(frame_dir, "frame-*.png")
    n_frames = len(glob.glob(frame_glob))

    def open_frame(frame_number):
        return Image.open(frame_filename_format.format(frame=frame_number + 1)) # ffmpeg counts from 1, grrr

    frame0 = open_frame(0)
    frame_width, frame_height = frame0.size

    def get_pixel(frame, x, y):
        # TODO: Just squishing everything into a cube is kinda lame...
        x = x * frame_width // 256
        y = y * frame_height // 256
        frame = frame * n_frames // 256
        if frame not in frame_cache:
            frame_cache[frame] = open_frame(frame).load()
        return frame_cache[frame][x, y]

    c = Image.new("RGB", map.dimensions())
    cd = ImageDraw.Draw(c)
    step = len(csource)/float(len(map))
    if quiet:
        prog = progress.Dummy()
    else:
        prog = progress.Progress(len(map))
    for i, p in enumerate(map):
        xyz = csource.point(int(i*step))
        color = get_pixel(*xyz)
        cd.point(tuple(p), fill=tuple(color))
        if not i % 100:
            prog.tick(i)
    c.save(name)


def main():
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(
                usage = "%prog [options] <input_directory> <output_image>",
                version="%prog 0.1",
            )
    parser.add_option(
        "-c", "--colorsource", action="store",
        type="str", dest="colorsource", default="hilbert"
    )
    parser.add_option(
        "-m", "--map", action="store",
        type="str", dest="map", default="hilbert"
    )
    parser.add_option(
        "-s", "--size", action="store",
        type="int", dest="size", default=512
    )
    parser.add_option(
        "-q", "--quiet", action="store_true",
        dest="quiet", default=False
    )
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error("Please specify input frame directory and output file.")

    csource = scurve.fromSize(options.colorsource, 3, 256**3)
    map = scurve.fromSize(options.map, 2, options.size**2)
    drawmap(map, csource, args[1], options.quiet, args[0])

if __name__ == "__main__":
    main()

