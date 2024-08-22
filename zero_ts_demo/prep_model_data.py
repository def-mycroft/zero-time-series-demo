
from .imports import * 
from . import helpers as hp

README = f"""
Electricity Demand Data from UCI Repository 

Created {pd.Timestamp.utcnow().isoformat()}. See URL {hp.DOCS_URL}. 

Each row here is a 15-minute interval and each value is kW used in that period.
Note that the original dataset has 370 columns (i.e. 370 energy clients). Some
of these have been removed due to having extreme outliers. Time series with
extreme outliers can be analyzed separately. 

"""


def calculate_z(X):
    """Given a series of data, calculate z-score metrics"""
    x = X[X > 0].copy().rename('kw')
    m = x.rolling(8).mean().rename('kw_rolling_mean')
    sl = pd.concat([x, m], axis=1).dropna().sort_index()
    sl['z_score'] = ((sl['kw'] - sl['kw_rolling_mean']) / sl['kw'].std()).abs()
    return sl


def summarize_anamolies(df):
    """Calculate maximum abs(z-score) for each column"""
    z_scores = dict()
    for col in df.columns:
        sl = calculate_z(df[col])
        z_scores[col] = sl['z_score'].max()
    return pd.Series(z_scores).sort_values()


def subset_data(df):
    """Select only time series with ceiling z-score"""
    zs = summarize_anamolies(df)
    cols = zs[zs < 4].index.tolist()
    return df[cols].copy()


def prep_write():
    """Prepare data for prediction task"""
    print('processing data...')
    df = (hp.load_base_data().pipe(subset_data)
            .reset_index(drop=False).sort_values(by=['date'])
            .drop(columns=['date']))
    print('done, writing data...')
    fpo = join(hp.PATH_DATA, 'model-data.csv')
    df.to_csv(fpo)
    print(f"wrote '{fpo}'")
    fpo = f"{os.path.splitext(fpo)[0]} - README.txt"
    with open(fpo, 'w') as f:
        f.write(README)
    print(f"wrote '{fpo}'")

    return df
