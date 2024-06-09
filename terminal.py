import argparse

from trading import alpaca_functions
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
    "-tr",
    "--trade",
    action="store_true",
    help="visit the trade menu for this ticker",
)
parser.add_argument(
    "-p",
    "--positions",
    action="store_true",
    help="print current positions",
)
parser.add_argument(
    "--exitall", action="store_true", help="exit all positions immediately"
)
parser.add_argument(
    "-im", "--imenu", action="store_true", help="enter interactive menu"
)
parser.add_argument(
    "-q", "--quote", action="store_true", help="get a quote for the ticker"
)
args = parser.parse_args()

# Entry into alpaca
alpaca = Alpaca()

if not args:
    print("You have entered no arguments, add -h to get help")

if args.quote:
    asset_price = get_asset_price(args.ticker)
    print(f"{args.ticker} is trading at {asset_price} ")
elif args.trade:
    alpaca_executor.terminal_market_trade_menu(args.ticker, alpaca)
elif args.positions:
    alpaca.print_positions()
elif args.exitall:
    alpaca.close_all_positions()
elif args.imenu:
    cli_menu.main()
