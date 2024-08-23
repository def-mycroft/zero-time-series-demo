
from .imports import * 

PATH_DATA = join(expanduser('~'), 'zero-ts-demo-data')


def load_model_data():
    fp = join(PATH_DATA, 'model-data.csv')
    if not exists(fp):
        msg = (f"must have path '{fp}', build by running "
               f"'zero-time-series-demo prep --model-data-pipeline")
        raise Exception(msg)
    df = pd.read_csv(fp).filter(regex='^mt_|date')
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df[sorted(df.columns)].sort_index()


def load_base_data():
    fp = join(PATH_DATA, 'LD2011_2014.csv.gz')
    if not exists(fp):
        msg = (f"must have path '{fp}', build by running "
               f"'zero-time-series-demo prep --model-data-pipeline")
        raise Exception(msg)
    df = pd.read_csv(fp, compression='gzip')
    df['date'] = pd.to_datetime(df['date'])

    return df.set_index('date').sort_index().copy()
