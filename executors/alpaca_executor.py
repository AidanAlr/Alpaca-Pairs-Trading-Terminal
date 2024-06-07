import os
import sys

from utils.formatting_and_logs import blue_bold_print
from trading.alpaca_functions import Alpaca, get_asset_price


def quote_menu():
    try:
        blue_bold_print("Quote Menu Selected")
        symbol = input("Please enter a symbol: ")
        print(f"Quote - {get_asset_price(symbol)}")
    except Exception as e:
        print(e)


def live_position_menu(alpaca: Alpaca):
    try:
        blue_bold_print("Current Positions - Live Portfolio")
        alpaca.live_profit_monitor(6)
    except Exception as e:
        print(e)


def manual_trade_menu(alpaca: Alpaca):
    try:
        blue_bold_print("Manual Trade Selected")
        blue_bold_print("To place a trade, please enter the following information:")
        order_type = input("Type (market/limit): ").lower()
        symbol = input("Symbol: ")
        print(f"Quote - {get_asset_price(symbol)}")

        side = input("Side (buy/sell): ").lower()

        # Validate input for quantity
        while True:
            qty = input("Quantity: ")
            if qty.isnumeric():
                qty = float(qty)
                break

        # Limit order input
        if order_type == "limit":
            limit_trade_menu(symbol, qty, side, alpaca)

        # Market order input
        elif order_type == "market":
            market_trade(symbol, qty, side, alpaca)

    except Exception as e:
        print(e)


def terminal_market_trade_menu(symbol, alpaca):
    blue_bold_print(f"Please enter the side of the trade (buy/sell)?")
    side = input("->").strip().lower()

    # Validate input for quantity
    while True:
        qty = input("Quantity: ")
        if qty.isnumeric():
            qty = float(qty)
            break

    if side in ["b", "buy"]:
        market_trade(symbol, qty, "buy", alpaca)
    elif side in ["s", "sell"]:
        market_trade(symbol, qty, "sell", alpaca)


def market_trade(symbol, qty, side, alpaca):
    total_order_cost = get_asset_price(symbol) * qty
    blue_bold_print(f"Total order cost: {round(total_order_cost, 2)}")
    confirm = input("Confirm order (y/n): ")
    if confirm.lower() == "y":
        alpaca.send_market_order(symbol, qty, side)


def limit_trade_menu(symbol, qty, side, alpaca):
    while True:
        limit_price = input("Limit Price: ")
        if limit_price.isnumeric():
            limit_price = float(limit_price)
            break

    blue_bold_print(
        "Would you like to add a take profit/stop loss to your order? (y/n)"
    )
    tp_sl_choice = input()
    if tp_sl_choice.lower() == "y":
        blue_bold_print("Please enter the take profit gain (Enter 1.05 for 5% tp) : ")
        tp = input()
        tp_price = limit_price * float(tp)
        blue_bold_print("Please enter the stop loss loss (Enter 0.95 for 5% sl) : ")
        sl = input()
        sl_price = limit_price * float(sl)

        alpaca.send_limit_order(
            symbol, qty, side, limit_price, stop_loss=sl_price, take_profit=tp_price
        )
    else:
        alpaca.send_limit_order(symbol, qty, side, limit_price)
