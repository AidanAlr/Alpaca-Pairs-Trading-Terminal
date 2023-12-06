import sys
import time

import pandas as pd
from alpaca.trading import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
import os

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'


class AlpacaClient:
    def __init__(self):
        self.client = self.connect_to_alpaca("PKNWSWFGL7X6F50PJ8UH", "1qpcAmhEmzxONh3Im0V6lzgqtVOX2xD3k7mViYLX", paper=True)
        self.in_position = bool(self.client.get_all_positions())
        self.positions = self.get_positions_df()

    def connect_to_alpaca(self, api_key: str, api_secret: str, paper: bool) -> TradingClient:
        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper)
            account = trading_client.get_account()

            print('Connected to ALPACA.')
            print(f'${account.buying_power} is available as buying power.')
            return trading_client

        except Exception:
            print("Issue connecting to ALPACA.")

    def enter_hedge_position(self, stock_1, stock_2, side, leverage, hr):

        if side == "buy":
            stock_1_side = OrderSide.BUY
            stock_2_side = OrderSide.SELL
        elif side == "sell":
            stock_1_side = OrderSide.SELL
            stock_2_side = OrderSide.BUY

        # Placing orders
        market_order = self.client.submit_order(
            order_data=self.client.MarketOrderRequest(
                symbol=stock_1,
                qty=1 * leverage,
                side=stock_1_side,
                time_in_force=TimeInForce.DAY
            ))
        print(stock_1 + ' ' + stock_1_side + 'order executed')

        # Placing Short Order using hedge ratio
        market_order_2 = self.client.submit_order(
            order_data=self.client.MarketOrderRequest(
                symbol=stock_2,
                qty=round(hr * leverage),
                side=stock_2_side,
                time_in_force=TimeInForce.DAY
            ))
        print(stock_2 + ' ' + stock_2_side + 'order executed')

    def get_positions_df(self):
        assets = pd.DataFrame()
        if self.in_position:
            for n in range(len(self.client.get_all_positions())):
                pos = dict(self.client.get_all_positions()[n])
                pos = pd.DataFrame.from_dict(pos, orient='index').T
                assets = pd.concat([assets, pos])

                # Changing columns from str to float type
                columns_to_convert = ['unrealized_pl', 'cost_basis', 'market_value',
                                      'avg_entry_price', 'qty', 'unrealized_plpc']
                for column in columns_to_convert:
                    assets[column] = assets[column].astype(float)

        return assets

    def unrealised_profit(self):
        pass

    def take_profit(self):
        pass
