
from .load_data import *

import inspect
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

