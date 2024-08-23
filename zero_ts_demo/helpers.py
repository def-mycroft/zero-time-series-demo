

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
    """In jupyter, display source of function"""
    x = inspect.getsource(func)
    x = f"```python\n{x}\n```"
    display(Markdown(x))


def create_project_folder():
    """As needed, create project data folder"""
    if not exists(PATH_DATA):
        x = input(f"Need a folder for data...create '{PATH_DATA}'? (y) > ")
        if x == 'y':
            cmd = f"mkdir -p '{PATH_DATA}'"
            ex(cmd)
            print(f"Ran '{cmd}'")


def create_image_grid(fig_list, cols, rows, resize=1, 
                      bg_color=(255, 255, 255)):
    """Concatenate a list of figures into a grid

    Parameters
    ----------

        fig_list : list of matplotlib.figure.Figure
            List of matplotlib figures to be arranged in a grid.
        cols : int
            Number of columns in the grid.
        rows : int
            Number of rows in the grid.
        resize : float, optional
            Scaling factor for resizing the final grid image (default is
            1).
        bg_color : tuple, optional
            Background color of the grid image as an RGB tuple (default
            is white: (255, 255, 255)).

    Returns
    -------
        PIL.Image.Image
            A PIL Image object representing the concatenated grid of
            figures.
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
