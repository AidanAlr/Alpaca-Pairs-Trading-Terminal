import os
import sys

import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import coint

# Directory Path Setup
""" Set up the directory path for the script and adjust sys.path for module imports. """
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Custom Module Imports
from utils.my_timer import timeit
from analysis.DATES import Dates
from analysis.errors import NoSuitablePairsError
from utils.formatting_and_logs import blue_bold_print, green_bold_print
from analysis.statistical_methods import run_adf_on_best_pairs

pd.set_option('mode.chained_assignment', None)


class StockData:
    """ A class for managing and analyzing stock data. """

    def __init__(self, asset_list, bypass_adf_test):
        """ Initializes the StockData object by downloading stock data, finding high correlation and cointegrated
        pairs, and determining the most suitable pair for analysis."""
        self.price_history_df = self.download_stock_data(asset_list)
        self.highest_corr_pairs_df = self.find_highest_corr_pairs(self.price_history_df)
        self.co_integrated_pairs_df = self.find_cointegrated_pairs(self.price_history_df, p_value_thresh=0.05)
        self.co_int_correlation_combined_df = self.combine_cointegration_correlation()
        if bypass_adf_test:
            self.adf_tested_df = self.co_int_correlation_combined_df
        else:
            self.adf_tested_df = self.filter_for_best_pairs()
        self.most_suitable_pair = self.find_most_suitable_pair()

    @timeit
    def download_stock_data(self, asset_list: list):
        """ Downloads the historical adjusted close prices of the stocks in the given asset list. """
        blue_bold_print("Starting data download...")
        end = Dates.END_DATE.value
        start = Dates.START_DATE.value
        prices_df = yf.download(tickers=asset_list, start=start, end=end)['Adj Close']
        prices_df = prices_df.dropna(axis=0)
        return prices_df

    @timeit
    def find_highest_corr_pairs(self, df):
        """ Identifies the highest correlation pairs from the given DataFrame. """
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
        """ Finds cointegrated pairs of stocks within a given DataFrame based on a specified p-value threshold. """
        n = len(df.columns)
        cointegrated_pairs_dict = {}

        for i in range(n):
            for j in range(i + 1, n):
                S1 = df.iloc[:, i]
                S2 = df.iloc[:, j]
                result = coint(S1, S2, trend="c", autolag="BIC")
                p_value = round(result[1], 5)
                if p_value <= p_value_thresh:
                    cointegrated_pairs_dict[f"{df.columns[i]} - {df.columns[j]}"] = p_value

        cointegrated_pairs_df = (pd.DataFrame.from_dict(cointegrated_pairs_dict, orient='index')
                                 .rename(columns={0: 'Cointegration'}))

        return cointegrated_pairs_df

    @timeit
    def combine_cointegration_correlation(self) -> pd.DataFrame:
        """ Combines cointegration and correlation data into a single DataFrame. """
        coint_corr_data = self.highest_corr_pairs_df.merge(self.co_integrated_pairs_df, left_on='lookup',
                                                           right_on=self.co_integrated_pairs_df.index)

        print(coint_corr_data)
        return coint_corr_data

    def filter_for_best_pairs(self):
        """ Filters the given DataFrame for the best pairs based on highest correlation and cointegration. """
        self.co_int_correlation_combined_df['adf_test'] = run_adf_on_best_pairs(self.co_int_correlation_combined_df)
        filtered_data = self.co_int_correlation_combined_df.query('adf_test == True')
        filtered_data = filtered_data.sort_values(by=['Correlation', 'Cointegration'], ascending=False)
        return filtered_data

    @timeit
    def find_most_suitable_pair(self) -> list:
        """ Identifies the most suitable stock pair based on highest correlation and cointegration criteria. Raises
        an error if no suitable pairs are found."""
        if len(self.adf_tested_df) < 2:
            raise NoSuitablePairsError
        stock_1 = self.adf_tested_df.iloc[0, 0]
        stock_2 = self.adf_tested_df.iloc[0, 1]
        return [stock_1, stock_2]
