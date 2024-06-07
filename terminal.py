import argparse

from trading.alpaca_functions import get_asset_price, Alpaca
from executors import cli_menu, alpaca_executor

parser = argparse.ArgumentParser()


parser.add_argument(
    "-t",
    "--ticker",
    type=str,
    help="enter an alpaca ticker and add -q -tr to quote or trade",
)
parser.add_argument(
    "-q", "--quote", action="store_true", help="get a quote for the ticker"
)
parser.add_argument(
    "-tr",
    "--trade",
    action="store_true",
    help="visit the trade menu for this ticker",
)
parser.add_argument(
    "-s", "--shell", action="store_true", help="enter interactive shell menu"
)
parser.add_argument(
    "-p",
    "--positions",
    action="store_true",
    help="enter live position menu i.e. see profit",
)
parser.add_argument(
    "--exitall", action="store_true", help="exit all positions immediately"
)
args = parser.parse_args()
alpaca_connection = Alpaca()

ticker = args.ticker
if args.quote:
    asset_price = get_asset_price(ticker)
    print(f"{ticker} is trading at {asset_price} ")
elif args.trade:
    alpaca_executor.terminal_market_trade_menu(ticker, alpaca_connection)
elif args.positions:
    alpaca_executor.live_position_menu(alpaca_connection)
elif args.exitall:
    alpaca_connection.close_all_positions()
elif args.shell:
    cli_menu.main()
