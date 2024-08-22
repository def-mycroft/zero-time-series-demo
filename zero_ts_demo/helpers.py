
import inspect
from IPython.display import Markdown

from .imports import * 

PATH_DATA = join(expanduser('~'), 'zero-ts-demo-data')
DOCS_URL = 'https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014'


def display_source(func):
    x = inspect.getsource(func)
    x = f"```python\n{x}\n```"
    display(Markdown(x))


def load_base_data():
    fp = join(PATH_DATA, 'LD2011_2014.csv.gz')
    if not exists(fp):
        msg = (f"must have path '{fp}', build by running "
               f"'zero-time-series-demo prep --download-base-data "
               f"--prep-base-data'")
        raise Exception(msg)
    df = pd.read_csv(fp, compression='gzip')
    df['date'] = pd.to_datetime(df['date'])

    return df.set_index('date').sort_index().copy()


def create_project_folder():
    if not exists(PATH_DATA):
        x = input(f"Need a folder for data...create '{PATH_DATA}'? (y) > ")
        if x == 'y':
            cmd = f"mkdir -p '{PATH_DATA}'"
            ex(cmd)
            print(f"Ran '{cmd}'")

