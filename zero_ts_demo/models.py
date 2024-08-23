
from .imports import * 
from matplotlib import pyplot as plt
from prophet import Prophet


class ProphetModel:
    """A prediction using Prophet model"""
    def __init__(self, sl_train, sl_test, title=''):
        self.sl_train = sl_train
        self.sl_test = sl_test
        self.title = title
        if not sl_train.columns.tolist() == sl_test.columns.tolist():
            raise Exception(f"Expect same columns for train and test.")
        if not sl_train.columns.tolist() == ['ds', 'y']:
            raise Exception('Expected columns ds, y. ')

    def fit_predict(self):
        """Fit model and return prediction"""
        self.model = Prophet()
        self.model.fit(self.sl_train)
        self.preds = (self.model.predict(self.sl_test.drop(columns='y'))
                          .merge(self.sl_test, on=['ds']))
        return self.preds

    def plot_preds(self):
        """Plot preds vs actual"""
        w = 15
        fs = (w, w/1.618)
        fig, ax = plt.subplots(figsize=fs)

        for col in ['yhat_upper', 'yhat_lower']:
            ax.plot(self.preds.index, self.preds[col], label=col, ls='--', 
                    color='#d0d0d0', linewidth=2)
        ax.plot(self.preds.index, self.preds['yhat'], label='yhat', ls='--', 
                color='grey', linewidth=3)
        ax.plot(self.preds.index, self.preds['y'], label='y', ls='solid', 
                color='black', linewidth=3)

        self.calculate_error()
        title = f"{self.title}\nrelative rmse: {self.rmse_relative:.3f}"
        ax.set_title(title)
        plt.legend()
        plt.grid()
        plt.close(fig)
        self.prediction_plot = fig

        return fig

    def calculate_error(self):
        rmse, rmse_relative = calculate_rmse(self.preds['y'], self.preds['yhat'])
        self.rmse = rmse
        self.rmse_relative = rmse_relative


def train_test(df, col, tail=0):
    """Split dataframe into train and test"""
    # create dataframe for prophet
    sl = df[[col]].reset_index().copy()
    sl.columns = ['ds', 'y']

    # index of first nonzero value in y
    idx = sl[sl['y'] > 0].index[0]
    if tail:
        # use only most recent rows for testing
        sl = sl.loc[idx:].tail(1000).copy()
    else:
        # use all data
        sl = sl.loc[idx:].copy()

    idx = 10
    idx_train = sl.index[:-idx]
    idx_test = sl.index[-idx:]
    sl_train = sl.loc[idx_train]
    sl_test = sl.loc[idx_test]

    return sl_train, sl_test


def calculate_rmse(y_actual, y_pred):
    """Calculate error metric given series of values"""
    rmse = np.sqrt(
        ((y_pred - y_actual)**2 / len(y_pred)).sum()
    )
    rmse_relative = rmse / y_actual.mean()
    return rmse, rmse_relative

