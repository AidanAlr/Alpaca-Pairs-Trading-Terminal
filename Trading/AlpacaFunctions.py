import sys
import time

import pandas as pd
from alpaca.trading.client import TradingClient
import os

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'


def connect_to_alpaca(api_key: str, api_secret: str, paper: bool) -> TradingClient:
    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper)
        account = trading_client.get_account()

        print('Connected to ALPACA.')
        print(f'${account.buying_power} is available as buying power.')
        return trading_client
    except Exception:
        print("Issue connecting to ALPACA.")


def gather_data(stock_1, stock_2):
    last_day = selected_df.tail(1)
    last_signal = last_day.signal.values[0]
    hr = round(last_day.hedge_ratio.values[0], 2)
    print('Analysed signals')


def pause_algo():
    for remaining in range(5 * 60 * 60, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Paused Algorithm ")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


def enter_long_hedge_position(stock_1, stock_2, leverage):
    # Placing Buy order of 1
    market_order = trading_client.submit_order(
        order_data=MarketOrderRequest(
            symbol=stock_1,
            qty=1 * leverage,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        ))
    print(stock_1 + ' LONG order executed')

    # Placing Short Order of Hedge Ratio Dot
    market_order_2 = trading_client.submit_order(
        order_data=MarketOrderRequest(
            symbol=stock_2,
            qty=round(hr * leverage),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        ))
    print(stock_2 + ' SHORT order executed')


def enter_short_hedge_position(stock_1, stock_2, leverage):
    # Placing Buy order of 1 AAVE
    market_order = trading_client.submit_order(
        order_data=MarketOrderRequest(
            symbol=stock_1,
            qty=1 * leverage,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        ))
    print(stock_1 + ' SHORT order executed')

    # Placing Short Order of Hedge Ratio Dot
    market_order = trading_client.submit_order(
        order_data=MarketOrderRequest(
            symbol=stock_1,
            qty=hr * leverage,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        ))

    print(stock_2 + ' LONG order executed')


def positions():
    assets = pd.DataFrame()
    if in_position():
        for n in range(len(trading_client.get_all_positions())):
            pos = dict(trading_client.get_all_positions()[n])
            pos = pd.DataFrame.from_dict(pos, orient='index').T
            assets = pd.concat([assets, pos])

            # Changin columns from str to float type
            columns_to_convert = ['unrealized_pl', 'cost_basis', 'market_value',
                                  'avg_entry_price', 'qty', 'unrealized_plpc']
            for column in columns_to_convert:
                assets[column] = assets[column].astype(float)
    return assets


def unrealised_profit(stock_1, stock_2):
    filtered_pos = positions()[positions()['symbol'].isin([stock_1, stock_2])]

    unrealised_profit = filtered_pos['unrealized_pl'].sum()
    cost_basis = filtered_pos['cost_basis'].sum()
    percent_profit = unrealised_profit / cost_basis

    return unrealised_profit, percent_profit


def take_profit(stock):
    side = str(positions().query("symbol == @stock")['side'][0])
    qty = str(positions().query("symbol == @stock")['qty'][0])

    def extract_position_side(string):
        return string.split('.')[-1]

    if side == 'PositionSide.LONG':
        market_order = trading_client.submit_order(
            order_data=MarketOrderRequest(
                symbol=stock,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            ))
        print('Sold ' + qty + ' shares of ' + stock + ' to exit ' + extract_position_side(side) + ' position')

    elif side == 'PositionSide.SHORT':
        market_order = trading_client.submit_order(
            order_data=MarketOrderRequest(
                symbol=stock,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            ))
        print('Longed ' + qty + ' shares of ' + stock + ' to exit ' + extract_position_side(side) + ' position')


def in_position():
    return bool(trading_client.get_all_positions())
