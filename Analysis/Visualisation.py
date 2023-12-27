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

    plt.show()


def zscored_spread(df):
    # Plot Z-scored spread
    df['z_score'].plot(figsize=(16, 4), color='orange')
    plt.title('Z-scored Spread')
    plt.axhline(1, color='k')
    plt.axhline(-1, color='k')
    plt.show()


def visualise_returns(df, tp, sl):
    # Trading Signal
    df['signal'] = df.apply(check_strategy_signal, axis=1)
    stock_1, stock_2 = get_tickers_from_collected_data_df(df)
    df['strategy_return'] = df[f'{stock_1}_forward_return'] * df['signal'] + \
                            df[f'{stock_2}_forward_return'] * df['signal'] * -df['hedge_ratio']
    df['signal'] = df.apply(lambda x: 1 if ((x['z_score'] < -1) or (x['combined_return'] > tp))
    else (-1 if ((x['zscored'] > 1) or (x['combined_return'] < sl)) else 0), axis=1)
    df['strategy_return'] = df[f'stock1_forward_return'] * df['signal'] + \
                            df[f'stock2_forward_return'] * df['signal'] * -df['hedge_ratio']



df_1 = collect_metrics_for_pair('AAPL', 'MSFT')
visualise_returns(df_1, 0.05, -0.05)
