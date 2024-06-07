import argparse

from trading.alpaca_functions import get_asset_price, Alpaca
from executors import cli_menu, alpaca_executor

parser = argparse.ArgumentParser()

parser.add_argument("--quote", type=str, help="enter the ticker you want a quote for")
parser.add_argument(
    "--trade", type=str, help="enter the ticker you want to place a market order for"
)
parser.add_argument("--shell", action="store_true", help="enter interactive shell menu")
parser.add_argument(
    "--positions", action="store_true", help="enter live position menu i.e. see profit"
)
parser.add_argument(
    "--exitall", action="store_true", help="exit all positions immediately"
)
args = parser.parse_args()
alpaca_connection = Alpaca()
if args.quote:
    asset_price = get_asset_price(args.quote)
    print(f"{args.quote} is trading at {str(asset_price)} ")
elif args.trade:
    alpaca_executor.manual_trade_menu(alpaca_connection)
elif args.positions:
    alpaca_executor.live_position_menu(alpaca_connection)

elif args.exitall:
    alpaca_connection.close_all_positions()

elif args.shell:
    cli_menu.main()
