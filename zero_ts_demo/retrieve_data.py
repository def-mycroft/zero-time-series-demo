
from .imports import * 
from . import helpers as hp

UCI_URLS = dict(
    electricityload=('https://archive.ics.uci.edu/static/public/321/'
                     'electricityloaddiagrams20112014.zip')
)


def retrieve_data():
    """Download raw data from UCI repo, unzip"""
    hp.create_project_folder()

    for k,url in UCI_URLS.items():
        fpo = join(hp.PATH_DATA, f"{k}.zip")
        if not exists(fpo):
            cmd = f"wget -O '{fpo}' {url}"
            ex(cmd)
            print(f"running '{cmd}'")
        else:
            print(f"have '{fpo}' already. ")

        assert exists(fpo), fpo
        cmd = f"unzip '{fpo}' -d '{hp.PATH_DATA}'"
        print(f"running '{cmd}'...")
        ex(cmd)
        print('done. ')
