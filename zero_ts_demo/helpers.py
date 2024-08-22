
from .imports import * 

PATH_DATA = join(expanduser('~'), 'zero-ts-demo-data')


def create_project_folder():
    if not exists(PATH_DATA):
        x = input(f"Need a folder for data...create '{PATH_DATA}'? (y) > ")
        if x == 'y':
            cmd = f"mkdir -p '{PATH_DATA}'"
            ex(cmd)
            print(f"Ran '{cmd}'")

