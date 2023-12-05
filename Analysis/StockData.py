from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import adfuller
import seaborn as sn
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
from scipy import stats
import websocket
import json
import time
from datetime import datetime
import sys

from Analysis import StatisticalMethods
from MyTimer import timeit
pd.set_option('mode.chained_assignment', None)


class StockData:
    def __init__(self, asset_list):
        self.price_history_df = self.download_stock_data(asset_list)
        self.highest_corr_pairs_df = self.find_highest_corr_pairs(self.price_history_df)
        self.cointegrated_pairs_df = self.find_cointegrated_pairs(self.price_history_df, p_value_thresh=0.05)
        self.coint_correlation_combined_df = self.combine_cointegration_correlation()

        # Adding the results of AD fuller to pairs_df
        self.coint_correlation_combined_df['adf_test'] = StatisticalMethods.run_adf_on_best_pairs(self.coint_correlation_combined_df)
        self.most_suitable_pair = self.find_most_suitable_pair()



    @timeit
    def download_stock_data(self, asset_list: list):
        # Setting dataset for the model
        end = dt.date.today()
        start = end - pd.DateOffset(days=365)
        prices_df = yf.download(tickers=asset_list, start=start, end=end)['Adj Close']
        prices_df = prices_df.dropna(axis=0)
        return prices_df

    @timeit
    def find_highest_corr_pairs(self, df):
        # Finding the highest correlation pairs
        corr_matrix = df.corr().abs()
        cmu = corr_matrix.unstack()
        cmu = cmu[cmu != 1]
        cmu = cmu[~cmu.duplicated()]
        cmu = cmu.sort_values(kind="quicksort", ascending=False)
        cmu = cmu.reset_index()
        cmu = cmu.rename(columns={"level_0": 'Stock_1', "level_1": 'Stock_2', 0: 'Correlation'})
        highest_corr_pairs = cmu[cmu['Correlation'] >= 0.80]
        highest_corr_pairs['lookup'] = highest_corr_pairs['Stock_1'] + ' - ' + highest_corr_pairs['Stock_2']
        return highest_corr_pairs

    @timeit
    def find_cointegrated_pairs(self, df, p_value_thresh):
        n = len(df.columns)
        coint_pairs_dict = {}
        for i in range(n):
            for j in range(i + 1, n):
                S1 = df.iloc[:, i]
                S2 = df.iloc[:, j]
                result = coint(S1, S2, trend="c", autolag="BIC")
                pvalue = round(result[1], 5)
                if pvalue <= p_value_thresh:
                    coint_pairs_dict[f"{df.columns[i]} - {df.columns[j]}"] = pvalue

        coint_pairs_df = pd.DataFrame.from_dict(coint_pairs_dict, orient='index').rename(columns={0: 'Cointegration'})
        return coint_pairs_df

    @timeit
    def combine_cointegration_correlation(self) -> pd.DataFrame:
        # Merge df of coint pairs above the threshold with df of highest correlation pairs
        coint_corr_data = self.highest_corr_pairs_df.merge(self.cointegrated_pairs_df, left_on='lookup', right_on=self.cointegrated_pairs_df.index)
        return coint_corr_data

    @timeit
    def find_most_suitable_pair(self):
        # Take the pair with the highest correlation in our dataset that meets our cointegration threshold
        stock_1 = self.coint_correlation_combined_df.iloc[0, 0]
        stock_2 = self.coint_correlation_combined_df.iloc[0, 1]
        print('Most Suitable Pair: ' + stock_1 + ' ' + stock_2)
        return [stock_1, stock_2]


