
from .imports import *


def prep_pipeline(sl, sample=0):
    """Apply prep steps

    If sample is not zero, rows will be sampled for 
    quicker development.

    """
    if sample:
        sl = sl.sample(sample)
    sl['date'] = pd.to_datetime(sl['date'])
    sl.columns = [x.lower() for x in sl.columns]
    for col in [x for x in sl.columns if x != 'date']:
        sl[col] = sl[col].astype(str).str.replace(',', '.').astype(float)
    return sl


def prep_write():
    """Prep input data and write out to file"""
    fp = join(os.path.expanduser('~'), 'zero-ts-demo-data', 'LD2011_2014.txt')
    print(f"loading base data from '{fp}'...")
    base_data = pd.read_csv(fp, sep=';', low_memory=False)
    print('done, manipulating...')
    df = (base_data.rename(columns={'Unnamed: 0':'date'})
                   .pipe(prep_pipeline).set_index('date').sort_index()
                   .reset_index().copy())
    fpo = f"{os.path.splitext(fp)[0]}.csv.gz"
    print(f"done, writing out data...")
    df.to_csv(fpo, compression='gzip', index=False)
    print(f"done, wrote '{fpo}'")

    return df

