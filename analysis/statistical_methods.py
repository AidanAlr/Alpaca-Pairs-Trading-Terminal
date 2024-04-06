import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import adfuller

# Directory Path Setup
"""Get the directory of the current script. If the script is not in the root directory, navigate to the root 
directory and append it to sys.path for module imports."""
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Custom Module Imports
from utils.my_timer import timeit
from analysis.DATES import Dates


def collect_metrics_for_pair(stock_1, stock_2) -> pd.DataFrame:
    """
    Downloads and processes financial data for a pair of stocks.
    Calculates returns, forward returns, hedge ratio using rolling OLS, spread, rolling correlation, and z-score.
    Classifies z-scores into trading signals.
    """

    # Downloading the required data
    stock_data_df = (
        yf.download(tickers=[stock_1, stock_2], start=Dates.START_DATE.value, end=Dates.END_DATE.value))
    stock_data_df = stock_data_df.stack()

    # Finding the required metrics
    stock_data_df['return'] = (stock_data_df['Adj Close'] - stock_data_df['Open']) / stock_data_df['Open']
    stock_data_df['forward_return'] = stock_data_df.groupby(level=1)['return'].transform(lambda x: x.shift(-1))
    stock_data_df = stock_data_df[['Adj Close', 'forward_return']].unstack().droplevel(axis=1, level=0)
    stock_data_df.columns = [stock_1, stock_2, f'{stock_1}_forward_return', f'{stock_2}_forward_return']
    stock_data_df[f'{stock_1}_return'] = np.log(stock_data_df[stock_1]).diff()
    stock_data_df[f'{stock_2}_return'] = np.log(stock_data_df[stock_2]).diff()

    # Calculating the hedge ration using a rolling OLS regression
    stock_data_df['hedge_ratio'] = RollingOLS(stock_data_df[f'{stock_2}_return'],
                                              stock_data_df[f'{stock_1}_return'],
                                              window=60).fit().params.values

    # Calculating the spread of stock 1 and stock 2 price
    stock_data_df['spread'] = (stock_data_df[stock_1] - stock_data_df[stock_2] * stock_data_df['hedge_ratio'])

    # Rolling Correlation test
    stock_data_df['roll_corr'] = stock_data_df[stock_1].rolling(180).corr(stock_data_df[stock_2])

    def smooth_zscore(spread):
        return (spread.rolling(1).mean() - spread.rolling(50).mean()) / spread.rolling(50).std()

    stock_data_df['z_score'] = smooth_zscore(stock_data_df['spread'])

    def classify_zscore(df: pd.DataFrame) -> int:
        if df['z_score'] < -1:
            return 1
        elif df['z_score'] > 1:
            return -1
        else:
            return 0

    # trading Signal
    stock_data_df['signal'] = stock_data_df.apply(classify_zscore, axis=1)

    return stock_data_df.dropna()


def adf_test(stock_1, stock_2) -> bool:
    """
    Performs the Augmented Dickey-Fuller test on the spread of two stocks to assess stationarity.
    Returns True if the spread is stationary, False otherwise.
    """
    removed_na_df = collect_metrics_for_pair(stock_1, stock_2)
    adf_result = adfuller(removed_na_df['spread'])[1]
    return adf_result <= 0.05


@timeit
def run_adf_on_best_pairs(highest_corr_pairs) -> list:
    try:
        """
        Applies the ADF test on pairs of stocks with the highest correlation.
        Returns a list of results indicating whether each pair's spread is stationary.
        """
        adf_list = []
        if len(highest_corr_pairs) != 0:
            for n in range(len(highest_corr_pairs)):
                result = adf_test(highest_corr_pairs['Stock_1'][n], highest_corr_pairs['Stock_2'][n])
                adf_list.append(result)
            return adf_list
    except Exception as e:
        print(e)
        return []
