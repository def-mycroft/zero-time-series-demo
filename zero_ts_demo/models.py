
from .imports import * 
from matplotlib import pyplot as plt
from statsmodels.tsa.ar_model import AutoReg, ar_select_order


class StatsmodelsARModel:
    """A prediction model using Statsmodels Autoregression (AR) model.

    This class encapsulates the process of fitting a Statsmodels AR
    model on the provided training data and making predictions on the
    test data.  The AR model automatically selects the autoregressive
    order based on the specified maximum lag.

    Attributes
    ----------
    sl_train : pandas.DataFrame
        The training data containing the time series to fit the model.
        Expected columns are 'ds' for datetime and 'y' for the value.
    sl_test : pandas.DataFrame
        The test data on which predictions will be made. The columns
        should match those in `sl_train`.
    title : str
        An optional title for the model or analysis.
    dynamic : bool
        Indicates whether dynamic predictions are used in the model, see
        method fit_predict. 
    y : pandas.Series
        The training data's 'y' values, with index reset for
        compatibility with Statsmodels.
    model : statsmodels.tsa.ar_model.AutoRegResultsWrapper
        The fitted Statsmodels AR model.
    preds : pandas.DataFrame
        A DataFrame containing the predictions and the corresponding
        test data.

    Methods
    -------
    fit_predict(maxlag=13, dynamic=True, **kwargs)
        Fit the Statsmodels AR model and make predictions on the test set.
    calculate_error()
        Placeholder for a method that calculates the prediction error.
    """
    def __init__(self, sl_train, sl_test, title=''):
        self.sl_train = sl_train
        self.sl_test = sl_test
        self.title = title
        if not sl_train.columns.tolist() == sl_test.columns.tolist():
            raise Exception(f"Expect same columns for train and test.")
        if not 'ds' in sl_train.columns and 'y' in sl_train.columns:
            raise Exception('Expected columns ds, y. ')

    def fit_predict(self, maxlag=13, dynamic=True, **kwargs):
        """Fit statsmodels AR model and make predictions on the test set.

        Statsmodels needs an index that starts at zero for training
        data. Therefore, note that the index of the training data
        dataframe is modified when feeding the training data into the AR
        model, and the index of the test data dataframe is modified
        accordingly.

        Parameters
        ----------
        maxlag : int, optional
            The maximum number of lags to consider when automatically
            selecting the autoregressive order (default is 13).
        dynamic : bool, optional
            Whether to use dynamic prediction, where the past predicted 
            values are used in place of actual values (default is True).
        **kwargs : 
            Additional arguments passed to the `ar_select_order`
            function.

        Returns
        -------
        None
            This method updates `self.preds` with the predictions, 
            adding a 'yhat' column to the test DataFrame.
        """
        self.dynamic = dynamic
        self.y = self.sl_train['y'].reset_index(drop=True)
        # setup the model, automatically finding the order 
        x = ar_select_order(self.y, maxlag=maxlag, **kwargs)
        self.model = x.model.fit()

        # setup predictions dataframe
        ## setup index
        idx_start = self.y.index[-1] + 1
        idx_end = idx_start + len(self.sl_test)
        idx = range(idx_start, idx_end)
        assert len(idx) == len(self.sl_test)
        self.sl_test.index = idx

        ## make prediction
        self.preds = self.sl_test.copy()
        self.preds['yhat_detrended'] = \
            self.model.predict(start=self.preds.index[0], 
                               end=self.preds.index[-1], dynamic=self.dynamic)
        self.preds['yhat'] = self.preds['yhat_detrended'] + \
            self.preds['y_trend']
        self.preds = (self.preds[['yhat', 'y_original', 'ds']]
                          .rename(columns={'y_original':'y'})
                          .copy())
        self.calculate_error()

    def plot_preds(self, plotwidth=12):
        """Plot predictions vs actual values in test set"""
        w = plotwidth
        fs = (w, w/1.618)
        fig, ax = plt.subplots(figsize=fs)

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
        """Calculate rmse metrics

        The metric `rmse_relative` is simply the RMSE divided by the
        mean of the test data. 

        """
        rmse, rmse_relative = \
            calculate_rmse(self.preds['y'], self.preds['yhat'])
        self.rmse = rmse
        self.rmse_relative = rmse_relative


def train_test(df, col, tail=0, rolling=5):
    """Split a DataFrame into training, test sets

    The function splits the input DataFrame into a training set and a 
    fixed-size test set of 5 units. Optionally, it can detrend the data 
    using a rolling mean.

    Assumes that `df` is a dataframe where each column is a different
    time series and that `col` specifies which series to analyze.  

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data to split.
    col : str
        The name of the column in `df` that contains the target 
        variable to be split.
    tail : int, optional
        If specified, only the most recent `tail` rows are used 
        for splitting (default is 0, meaning all data is used).
    rolling : int, optional
        The window size for calculating the rolling mean to 
        detrend the data (default is 5). If set to 0, no detrending 
        is applied.

    Returns
    -------
    sl_train : pandas.DataFrame
        The training set DataFrame.
    sl_test : pandas.DataFrame
        The test set DataFrame, with a fixed size of 5 units.
    """
    # create dataframe for prophet
    sl = df[[col]].reset_index().copy()
    sl.columns = ['ds', 'y']

    # index of first nonzero value in y
    idx = sl[sl['y'] > 0].index[0]
    if tail:
        # use only most recent rows for testing
        sl = sl.loc[idx:].tail(int(tail)).copy()
    else:
        # use all data
        sl = sl.loc[idx:].copy()

    if rolling:
        # detrend data
        sl['y_trend'] = sl['y'].rolling(rolling).mean()
        sl['y_detrended'] = sl['y'] - sl['y_trend']
        sl['y_original'] = sl['y'].copy()
        sl['y'] = sl['y_detrended'].copy()
        sl = sl.dropna(subset=['y_detrended'])


    # split train/test
    idx = 5
    idx_train = sl.index[:-idx]
    idx_test = sl.index[-idx:]
    sl_train = sl.loc[idx_train]
    sl_test = sl.loc[idx_test]

    if rolling:
        # forward fill the trend data in test
        # this is to avoid using unknowable data in the prediction
        sl_test['y_trend'] = sl_test['y_trend'].iloc[0]

    return sl_train, sl_test


def calculate_rmse(y_actual, y_pred):
    """Calculate error metric given series of values"""
    rmse = np.sqrt(
        ((y_pred - y_actual)**2 / len(y_pred)).sum()
    )
    rmse_relative = rmse / y_actual.mean()
    return rmse, rmse_relative
