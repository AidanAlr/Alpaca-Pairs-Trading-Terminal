import numpy as np
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import adfuller

from Analysis.Dates import Dates


def collect_metrics_for_pair(stock_1, stock_2):
    # Downloading the required data
    stock_data_df = yf.download(tickers=[stock_1, stock_2], start=Dates.START_DATE.value, end=Dates.END_DATE.value)
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

    # Smoothed Z Score
    stock_data_df['z_score'] = stock_data_df.apply(lambda x: x['spread'].rolling(1).mean() - x['spread'].rolling(50).mean() / x['spread'].rolling(50).std())

    # Trading Signal
    stock_data_df['signal'] = stock_data_df.apply(lambda x: 1 if (x['z_score'] < -1) else (-1 if (x['z_score'] > 1) else 0), axis=1)

    return stock_data_df


def adf_test(stock_1, stock_2):
    removed_na_df = collect_metrics_for_pair(stock_1, stock_2).dropna()
    adf_result = adfuller(removed_na_df['spread'])[1]

    if adf_result <= 0.05:
        return 'P-Value: ' + str(round(adf_result, 2)) + ' - Passed'
    else:
        return 'P-Value: ' + str(round(adf_result, 2)) + ' - Failed'


def run_adf_on_best_pairs(highest_corr_pairs):
    # Running ADF test
    adf_list = []
    for n in range(len(highest_corr_pairs)):
        result = adf_test(highest_corr_pairs['Stock_1'][n], highest_corr_pairs['Stock_2'][n])
        adf_list.append(result)

    return adf_list

