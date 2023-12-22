import sys
import time
import pandas as pd
from alpaca.trading import OrderSide, TimeInForce, PositionSide
from alpaca.trading.client import TradingClient
from alpaca.trading.stream import TradingStream
from alpaca.trading.requests import MarketOrderRequest
import os

sys.path.append("/Users/aidanalrawi/PycharmProjects/Pairs-Trading-Algorithm")

from AidanUtils.MyTimer import timeit

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'


def connect_to_trading_stream():
    """
    Connects to the Alpaca Trading Stream using predefined API credentials.
    Returns a TradingStream object if successful, else prints an error message.
    """
    try:
        return TradingStream("PKNWSWFGL7X6F50PJ8UH", "1qpcAmhEmzxONh3Im0V6lzgqtVOX2xD3k7mViYLX", paper=True)
    except Exception:
        print("Error getting trade stream")


def pause_algo(minutes):
    for remaining in range(minutes * 60 * 60, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Paused Algorithm: {:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


class Alpaca:
    """
    Alpaca class to manage trading activities.
    It handles connection to Alpaca API, managing positions, entering hedge positions,
    retrieving and displaying position data, profit calculation, and order management.
    """

    def __init__(self):
        """
        Constructor for Alpaca class.
        Initializes connection to Alpaca API, retrieves current positions,
        and sets up trading stream.
        """
        self.connected = False
        self.account = None
        self.client = self.connect_to_alpaca("PKNWSWFGL7X6F50PJ8UH", "1qpcAmhEmzxONh3Im0V6lzgqtVOX2xD3k7mViYLX",
                                             paper=True)
        self.in_position = bool(self.client.get_all_positions())
        self.positions = self.client.get_all_positions()

    @timeit
    def connect_to_alpaca(self, api_key: str, api_secret: str, paper: bool) -> TradingClient:
        """
        Establishes a connection to the Alpaca trading service using API credentials.
        If successful, prints the connection status and available buying power.
        Returns a TradingClient object.

        Args:
        api_key (str): Alpaca API key.
        api_secret (str): Alpaca API secret.
        paper (bool): Flag for paper trading (True for paper trading, False for live trading).

        Returns:
        TradingClient: A client object to interact with Alpaca's trading services.
        """
        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper)
            self.account = trading_client.get_account()
            print('Connected to Alpaca, buying power is: ' + self.account.buying_power)
            self.connected = True
            return trading_client
        except Exception:
            print("Error connecting to Alpaca")

    def enter_hedge_position(self, stock_1, stock_2, side, leverage, hr):
        """
        Enters a hedge position by placing market orders on two stocks.
        A hedge position involves buying one stock and selling another.

        Args:
        stock_1 (str): Symbol of the first stock.
        stock_2 (str): Symbol of the second stock.
        side (str): 'buy' or 'sell', indicating the direction of the hedge.
        leverage (float): Leverage factor to apply to the order quantity.
        hr (float): Hedge ratio to calculate the quantity of the second stock.
        """
        if side == "buy":
            stock_1_side = OrderSide.BUY
            stock_2_side = OrderSide.SELL
        elif side == "sell":
            stock_1_side = OrderSide.SELL
            stock_2_side = OrderSide.BUY

        try:
            # Placing market orders for both stocks
            market_order = self.client.submit_order(
                order_data=MarketOrderRequest(
                    symbol=stock_1,
                    qty=1 * leverage,
                    side=stock_1_side,
                    time_in_force=TimeInForce.DAY
                ))
            print(stock_1 + ' ' + stock_1_side + ' order executed')

            market_order_2 = self.client.submit_order(
                order_data=MarketOrderRequest(
                    symbol=stock_2,
                    qty=round(hr * leverage),
                    side=stock_2_side,
                    time_in_force=TimeInForce.DAY
                ))
            print(stock_2 + ' ' + stock_2_side + ' order executed')
        except Exception:
            print("Error entering hedge position")

    def get_positions_df(self):
        """
        Retrieves and formats the current positions into a DataFrame.
        Converts specific string columns to float for numerical analysis.
        Returns a DataFrame of the current positions.

        Returns:
        pandas.DataFrame: DataFrame containing details of current positions.
        """
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

    def print_positions(self):
        """
        Prints the details of the current positions held.
        Includes the side (Long/Short), quantity, purchase price, and unrealized profit percentage.
        """
        portfolio = self.client.get_all_positions()
        side_map = {PositionSide.SHORT: "Short", PositionSide.LONG: "Long"}
        print("Current Positions:")
        for position in portfolio:
            print("{} {} shares of {} purchased for {} current unrealised profit_pc is {}%"
                  .format(side_map[position.side],
                          position.qty.replace("-", ""),
                          position.symbol,
                          abs(float(position.cost_basis)),
                          self.get_unrealised_profit_pc()))

    def get_unrealised_profit_pc(self):
        """
        Calculates the percentage of unrealized profit or loss across all positions.
        Returns the percentage value rounded to three decimal places.

        Returns:
        float: The percentage of unrealized profit or loss.
        """
        try:
            portfolio = self.client.get_all_positions()
            profit = sum([position.unrealized_pl for position in portfolio])
            cost_basis = sum([position.cost_basis for position in portfolio])

            if cost_basis == 0:
                return 0

            return round((profit * 100 / cost_basis), 3)

        except Exception:
            pass

    def take_profit(self, tp):
        """
        Executes orders to take profit if the unrealized profit percentage exceeds the specified threshold.

        Args:
        tp (float): The profit threshold percentage to trigger selling.
        """
        if self.get_unrealised_profit_pc() > tp:
            print("Executing orders to take profit...")
            if self.close_all_positions():
                print("Took profit")

    def stop_loss(self, sl):
        """
        Executes stop loss orders if the unrealized loss exceeds the specified threshold.

        Args:
        sl (float): The loss threshold percentage to trigger selling.
        """
        sl = abs(sl) * -1
        if self.get_unrealised_profit_pc() < sl:
            print("Executing orders to stop loss")
            if self.close_all_positions():
                print("Stopped Loss")

    def close_all_positions(self):
        """
        Closes all positions by submitting market or limit orders.
        If unable to submit a market order, it submits a limit order at the current price.
        Returns True if all orders are filled, False otherwise.

        Returns:
        bool: True if all positions are closed successfully, False otherwise.
        """
        close_info = self.client.close_all_positions(cancel_orders=True)
        for order in close_info:
            order = order.body
            side_map = {OrderSide.BUY: "buy", OrderSide.SELL: "sell"}
            print(
                f"Attempted to {side_map[order.side]} {order.qty} shares of {order.symbol}. {order.filled_qty} orders filled for {order.filled_avg_price}")
            if order.filled_qty == order.qty:
                return True
            else:
                return False

    def use_live_tp_sl(self, tp, sl):
        """
        Continuously monitors the portfolio for take profit (tp) or stop loss (sl) conditions.
        Prints the current unrealized profit percentage and executes orders if conditions are met.

        Args:
        tp (float): Take profit threshold percentage.
        sl (float): Stop loss threshold percentage.
        """
        print("Take Profit:" + str(tp) + "%")
        print("Stop Loss:" + str(abs(sl) * -1) + "%")
        self.print_positions()
        count = 0
        while True:
            # if keyboard.is_pressed('space'):  # Check if space bar is pressed
            #     print("\nPausing algorithm...")
            #     pause_algo(10)  # Call the pause_algo method
            #     break  # Break out of the loop to pause the algorithm

            output = f'{count}_Current Profit: {self.get_unrealised_profit_pc()} %'
            self.stop_loss(sl)
            self.take_profit(tp)
            sys.stdout.write("\r" + output.ljust(50))  # Overwrite the line with padding
            sys.stdout.write("Press space to pause the algorithm")

            time.sleep(1)
            sys.stdout.flush()
            count += 1
