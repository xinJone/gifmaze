# -*- coding: utf-8 -*-
"""
This script combines two algorithms together in one animation.
It has full 256 colors in the global color table.
"""
from colorsys import hls_to_rgb
import gifmaze as gm
from gifmaze.algorithms import random_dfs, astar


# firstly define the size and color_depth of the image.
width, height = 600, 400
color_depth = 2

# define a surface to draw on.
surface = gm.GIFSurface(width, height, color_depth, bg_color=0)

palette = [0, 0, 0, 200, 200, 200, 255, 0, 255, 150, 200, 100]
for i in range(256):
    rgb = hls_to_rgb((i / 360.0) % 1, 0.5, 1.0)
    palette += [int(round(255 * x)) for x in rgb]

surface.set_palette(palette)

# next define an animation environment to run the algorithm.
anim = gm.Animation(surface)

# set the speed, delay, and transparent color we want.
anim.set_control(speed=20, delay=5, trans_index=3)


# `region=5` means the maze is padded with border of 5 pixels.
maze = anim.create_maze_in_region(cell_size=5, region=5, mask=None)

# in the first algorithm only 4 colors occur in the image, so we can use
# a smaller minimum code length.
surface.set_lzw_compress(2)
# pad two seconds delay, get ready!
anim.pad_delay_frame(200)

# the animation runs here.
random_dfs(maze, start=(0, 0))

# pad three seconds delay to see the result clearly.
anim.pad_delay_frame(300)

# now we run the maze solving algorithm.
# this time we use full 256 colors, hence the minimum code length is 8.
surface.set_lzw_compress(8)

# the tree and wall are unchanged throughout the maze solving algorithm hence
# it's safe to use 0 as the transparent color and color the wall and tree transparent.
anim.set_colormap({0: 0, 1: 0, 2: 2, 3: 3})
anim.set_control(speed=10, delay=5, trans_index=0)

# run the maze solving algorithm.
astar(maze,
      start=(0, 0),
      end=(maze.size[0] - 1, maze.size[1] - 1))

# pad five seconds delay to see the path clearly.
anim.pad_delay_frame(500)

# save the result.
surface.save('randomdfs_astar.gif')

surface.close()
