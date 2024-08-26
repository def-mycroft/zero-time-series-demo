
from .imports import * 
from matplotlib import pyplot as plt


def rolling_window_variance(df, col, mstd_window=30, ma_window=3):
    """Setup a series with rolling window standard deviation"""
    y = df[col].copy()
    idx = y[y != 0].index[0]
    y = y[idx:].reset_index()
    y = (y.rename(columns={col:'y'}).sort_values(by=['date'])
          .reset_index(drop=True))

    # detrend using simple moving average 
    y['y_mean'] = y['y'].rolling(ma_window).mean()
    y['y'] = y['y'] - y['y_mean']

    y['std_rolling'] = y['y'].rolling(mstd_window).std()

    return y.dropna(subset=['std_rolling'])


def plot(y, w=12, tail=1000):
    """Plot value and rolling window std"""
    fig, (axu, axl) = plt.subplots(2, 1, figsize=(w, w/1.618))
    d = y.tail(tail)
    x = d.index
    axu.plot(x, d['y'])
    axu.set_title('Detrended Series')
    axl.plot(x, d['std_rolling'])
    axl.set_title('Moving Window Standard Deviation')

    plt.tight_layout()
    plt.close(fig)

    return fig

