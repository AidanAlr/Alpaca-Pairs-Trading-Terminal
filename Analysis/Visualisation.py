import os
import sys
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# If the script is not in the root directory, navigate to the root directory
root_dir = os.path.dirname(current_dir)
# Append the root directory to sys.path so that modules can be imported
sys.path.append(root_dir)

import numpy as np
from matplotlib import pyplot as plt
from Analysis.StatisticalMethods import classify_zscore, collect_metrics_for_pair


def get_tickers_from_collected_data_df(df):
    tickers = []
    for column in df.columns:
        if column.endswith('_forward_return'):
            tickers.append(column.split('_')[0])
    return tickers[0], tickers[1]


def spread_visualisation(df):
    stock_1, stock_2 = get_tickers_from_collected_data_df(df)
    hedge_ratio = round(df['hedge_ratio'].iloc[-1], 2)
    plt.title(f'{stock_1}-{hedge_ratio}*{stock_2}')
    df['spread'].plot(figsize=(16, 4), color='red')
    plt.show()


def zscored_spread(df):
    df['zscored'].plot(figsize=(16, 4), color='orange')
    plt.title('Zscored Spread')
    plt.axhline(1, color='k')
    plt.axhline(-1, color='k')
    plt.show()


def visualise_returns(df, tp, sl):
    stock_1, stock_2 = get_tickers_from_collected_data_df(df)
    df = df.dropna()
    df['combined_return'] = df[f'{stock_1}_return'] + df[f'{stock_2}_return'] * df['hedge_ratio']

    def check_strategy_signal(df):
        if df['combined_return'] > tp or df['z_score'] < -1:
            return 1
        elif df['combined_return'] < sl or df['z_score'] > 1:
            return -1
        else:
            return 0

    # Trading Signal
    df['signal'] = df.apply(check_strategy_signal, axis=1)
    df['strategy_return'] = df[f'{stock_1}_forward_return'] * df['signal'] + \
                            df[f'{stock_2}_forward_return'] * df['signal'] * -df['hedge_ratio']

    portfolios_cumulative_return = np.exp(np.log1p(df['strategy_return']).cumsum())
    portfolios_cumulative_return.plot(figsize=(16, 6), color='red')
    plt.title('Strategy Cumulative Returns')
    plt.ylabel('Return')
    plt.show()


df_1 = collect_metrics_for_pair('AAPL', 'MSFT')
visualise_returns(df_1, 0.05, -0.05)