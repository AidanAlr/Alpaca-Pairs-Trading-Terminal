import sys

import numpy as np
from matplotlib import pyplot as plt
sys.path.append("/Users/aidanalrawi/PycharmProjects/Pairs-Trading-Algorithm")


ax = ('TECK', 'WPM')[['TECK', 'WPM']].plot(
    figsize=(12, 6))  # , title = 'Daily Closing Prices for {} and {}'.format(asset1,asset2))
ax.set_ylabel("Closing Price")
ax.grid(True);


def spread_visualisation(df):
    plt.title(f'stock1-{round(df.hedge_ratio[-1], 2)}*stock2')
    df['spread'].plot(figsize=(16, 4), color='red')


def zscored_spread(df):
    df['zscored'].plot(figsize=(16, 4), color='orange')
    plt.title('Zscored Spread')
    plt.axhline(1, color='k')
    plt.axhline(-1, color='k')


def visualise_returns(df, tp, sl):
    df = df.dropna()
    df['combined_return'] = df[f'stock1_return'] + df[f'stock2_return']
    # Trading Signal
    df['signal'] = df.apply(lambda x: 1 if ((x['zscored'] < -1) or (x['combined_return'] > tp))
    else (-1 if ((x['zscored'] > 1) or (x['combined_return'] < sl)) else 0), axis=1)
    df['strategy_return'] = df[f'stock1_forward_return'] * df['signal'] + \
                            df[f'stock2_forward_return'] * df['signal'] * -df['hedge_ratio']

    portfolios_cumulative_return = np.exp(np.log1p(df['strategy_return']).cumsum())
    portfolios_cumulative_return.plot(figsize=(16, 6), color='red')
    plt.title('Strategy Cumulative Returns')
    plt.ylabel('Return')
    plt.show()
