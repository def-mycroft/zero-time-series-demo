
from .load_data import *

import inspect
import tempfile
from copy import deepcopy as copy
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw
from IPython.display import Markdown

from .imports import * 

PATH_DATA = join(expanduser('~'), 'zero-ts-demo-data')
DOCS_URL = 'https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014'


def display_source(func):
    x = inspect.getsource(func)
    x = f"```python\n{x}\n```"
    display(Markdown(x))


def create_project_folder():
    if not exists(PATH_DATA):
        x = input(f"Need a folder for data...create '{PATH_DATA}'? (y) > ")
        if x == 'y':
            cmd = f"mkdir -p '{PATH_DATA}'"
            ex(cmd)
            print(f"Ran '{cmd}'")


def create_image_grid(fig_list, cols, rows, resize=1, 
                      bg_color=(255, 255, 255)):
    """Concatenate a list of figures into a grid

    Assumes that all figures are exactly the same size. 

    image_list should be a list of matplotlib.figure.Figure objects. 

    """
    image_list = [fig_to_pil(x) for x in fig_list]
    # get size of 'cell' images, assume that all images are the same size
    width, height = image_list[0].size
    # calculate pixel size of entire output image
    grid_width = cols * width
    grid_height = rows * height

    grid_image = Image.new('RGB', (grid_width, grid_height), color=bg_color)

    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if idx < len(image_list):
                grid_image.paste(image_list[idx], (j*width, i*height))

    # resize image
    size = (int(grid_width*resize), int(grid_height*resize))
    grid_image = grid_image.resize(size)

    return grid_image


def fig_to_pil(fig):
    """Convert a matplotlib fig to a PIL Image"""
    # write to a temp directory
    temp_dir = tempfile.gettempdir()
    fp = join(temp_dir, 'zero-ts-demo.png')
    if exists(fp):
        os.remove(fp)
    fig.savefig(fp)
    # then load image from path
    img = Image.open(fp)

    return img
