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
from Analysis import StatisticalMethods
from Analysis.StockData import StockData

# # In order to perform analysis from here and import the most suitable pair
# SYMBOLS_LIST = ['XOM', 'CVX', 'BP', 'COP', 'PXD', 'EOG', 'APA', 'OXY', 'MPC', 'SLB', 'HAL', 'KMI', 'PBR', 'SU', 'ENB',
#                 'EPD', 'EQT', 'BHP',
#                 'FCX', 'NEM', 'GOLD', 'WPM', 'AGI', 'TECK', 'SBSW', 'CF', 'ADM', 'MOS', 'FMC', 'LIN', 'NUE', 'RGLD',
#                 'WY', 'PAA', 'ET',
#                 'MPLX',
#                 'WMB', 'X', 'AA', 'CMP', 'IP', 'PKG', 'PPG']
# stock_data = StockData(SYMBOLS_LIST)
# most_suitable_pair = stock_data.find_most_suitable_pair()

# Otherwise just state pair here 
most_suitable_pair = ['EPD', 'PAA']

# Get DF using function in StatisticalMethods.py
stock_data_df = StatisticalMethods.collect_metrics_for_pair(most_suitable_pair[0], most_suitable_pair[1])


def plot_tickers(df):
    # Plot closing prices over time for each stock
    plt.plot(df.index, df.iloc[:, 0], label ='Stock 1: ' + df.columns[0])
    plt.plot(df.index, df.iloc[:, 1], label ='Stock 2: ' + df.columns[1])

    plt.title('Stock Pair Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')

    plt.legend()
    plt.show()


def spread_visualisation(df):
    #Plot spread of the pair over time
    plt.title(df.columns[0] + '-' + df.columns[1] + ' ' + 'Spread')
    df['spread'].plot(figsize=(16, 4), color='red')

    plt.show()


def zscored_spread(df):
    # Plot Z-scored spread
    df['z_score'].plot(figsize=(16, 4), color='orange')
    plt.title('Z-scored Spread')
    plt.axhline(1, color='k')
    plt.axhline(-1, color='k')

    plt.show()


def visualise_returns(df):
    tp = df.columns[0]
    sl = df.columns[1]
    df = df.dropna()
    df['combined_return'] = df[f'stock1_return'] + df[f'stock2_return']
    # Trading Signal
    df['signal'] = df.apply(lambda x: 1 if ((x['z_score'] < -1) or (x['combined_return'] > tp))
    else (-1 if ((x['zscored'] > 1) or (x['combined_return'] < sl)) else 0), axis=1)
    df['strategy_return'] = df[f'stock1_forward_return'] * df['signal'] + \
                            df[f'stock2_forward_return'] * df['signal'] * -df['hedge_ratio']

    portfolios_cumulative_return = np.exp(np.log1p(df['strategy_return']).cumsum())
    portfolios_cumulative_return.plot(figsize=(16, 6), color='red')
    plt.title('Strategy Cumulative Returns')
    plt.ylabel('Return')
    plt.show()

plot_tickers(stock_data_df)