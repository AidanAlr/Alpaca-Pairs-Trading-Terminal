import os
import sys
import time
from typing import List, Tuple, Optional

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from analysis.statistical_methods import collect_metrics_for_pair
from executors.cli_controller import main_menu
from analysis.visualisation import spread_visualisation, zscored_spread, visualise_returns
from analysis.errors import NoSuitablePairsError
from analysis.stock_data import StockData
from utils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print
from utils.formatting_and_logs import CustomFormatter
import logging

from trading.alpaca_functions import Alpaca

# Configure logging with a custom formatter
logging.basicConfig(level=logging.INFO)
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.handlers = [handler]


def read_tickers_from_file(path: str) -> Optional[List[str]]:
    """
    Reads ticker symbols from a file and returns them as a list.
    Args:
    path (str): File path to read ticker symbols.
    Returns:
    Optional[List[str]]: List of ticker symbols, or None if file not found.
    """
    try:
        with open(path, 'r') as file:
            return [ticker.strip() for ticker in file.read().split(',') if len(ticker.strip()) > 1]
    except FileNotFoundError:
        logging.error("File not found. Please try again.")
        return None


def process_stock_data(symbols_list: List[str]) -> Optional[Tuple[str, str]]:
    """
    Processes stock symbols to find the most suitable pair for analysis.
    Args:
    symbols_list (List[str]): List of stock ticker symbols.
    Returns:
    Optional[Tuple[str, str]]: Most suitable pair of stocks, or None if no suitable pair is found.
    """
    try:
        stock_data = StockData(asset_list=symbols_list, bypass_adf_test=False)
        red_bold_print("Most Suitable Pair: " + stock_data.most_suitable_pair)
        return stock_data.most_suitable_pair
    except NoSuitablePairsError:
        logging.warning("No suitable pairs found. Option to bypass adf_test is available but not recommended (y/n): ")
        bypass_adf_test = input()
        if bypass_adf_test.lower() == 'y':
            stock_data = StockData(asset_list=symbols_list, bypass_adf_test=True)
            red_bold_print(
                "Most Suitable Pair: {}, {}".format(stock_data.most_suitable_pair[0], stock_data.most_suitable_pair[1]))
            return stock_data.most_suitable_pair
        else:
            print("There are no suitable pairs and you wont bypass the adf test.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def run_analysis() -> None:
    """
    Initiates the stock analysis process by reading ticker symbols and processing them.
    """
    while True:
        try:
            blue_bold_print("Ticker symbols list must be in a csv file.")
            blue_bold_print("Please enter the absolute path to a csv file containing a list of ticker symbols, leaving this blank will use the default symbols.csv or enter b to go "
                            "back:")
            path = input()
            if path == 'b':
                main_menu(alpaca=Alpaca())
            if not path:
                print(root_dir)
                path = os.path.join(root_dir, 'symbols.csv')

            symbols_list = read_tickers_from_file(path)
            logging.info("Tickers to analyse: " + str(symbols_list))
            most_suitable_pair = process_stock_data(symbols_list)

            if symbols_list is not None and most_suitable_pair is not None:
                strategy_info = collect_metrics_for_pair(most_suitable_pair[0], most_suitable_pair[1])
                print(strategy_info)
                hedge_ratio = strategy_info['hedge_ratio'].iloc[0]
                print("Hedge Ratio: " + str(hedge_ratio))
                blue_bold_print("Would you like to visualise/backtest this strategy? type(y/n) ")

                if input().lower() == 'y':
                    backtest_strategy(most_suitable_pair)
                else:
                    main_menu(alpaca=Alpaca())
                break
        except Exception as e:
            print(e)

def check_signal(pair: List):
    strategy_info = collect_metrics_for_pair(pair[0], pair[1])
    signal = strategy_info.tail(1)['signal'].item()
    signal_string = "Long" if signal == 1 else "Short" if signal == -1 else "Neutral"
    red_bold_print(f"The signal is {signal_string} on this pair.")
    return signal


def execute_pairs_strategy(pair: List):
    alpaca = Alpaca()
    if alpaca.in_position:
        red_bold_print("You are currently in a position, please exit the position before executing a new strategy.")
    else:
        if not pair:
            try:
                blue_bold_print("Please enter the pair you would like use in the format stock_1, stock_2:")
                pair_input = input()
                pair = [pair.strip() for pair in pair_input.split(',')]
                logging.info(f"Tickers to execute strategy are: {pair[0]} and {pair[1]}")
                strategy_info = collect_metrics_for_pair(pair[0], pair[1])
                hedge_ratio = strategy_info['hedge_ratio'].iloc[0]
                logging.info("The hedge ratio for this pair is: " + str(hedge_ratio))
                leverage = float(input("Please enter your selected leverage:"))
                red_bold_print("Enter your take profit and stop loss in the format 0.1, 0.05")
                tp, sl = input().split(',')
                tp = float(tp.strip())
                sl = float(sl.strip())
                confirmed = input("Type confirm to execute the strategy, type anything else to abort and return "
                                  "to main menu ").lower() == 'confirm'
                if confirmed:

                    while True:

                        # Profit and loss monitoring
                        if alpaca.check_and_stop_loss(sl) or alpaca.check_and_take_profit(tp):
                            "This strategy has exited due to take profit or stop loss."
                            break

                        signal = check_signal(pair)

                        if alpaca.in_position:
                            logging.info("You are currently in a position so will not execute a new trade.")

                            if signal == 0:
                                logging.info("Analysis wants to exit positions.")
                                for symbol in pair:
                                    alpaca.close_position_for_symbol(symbol)

                        elif not alpaca.in_position:
                            match signal:
                                case 1:
                                    logging.info("Analysis has deemed an opportunity for a long hedge position")
                                    alpaca.enter_hedge_position(pair[0], pair[1],
                                                                side="buy", hr=hedge_ratio, leverage=leverage)
                                case -1:
                                    logging.info("Analysis has deemed an opportunity for a short hedge position")
                                    alpaca.enter_hedge_position(pair[0], pair[1],
                                                                side="sell", hr=hedge_ratio, leverage=leverage)

                        # Displaying live profit and sleeping for 60 seconds
                        alpaca.live_profit_monitor(30)


            except Exception as e:
                print(e)


def backtest_strategy(pair: List or Tuple) -> None:
    """
    Backtests a trading strategy based on user choices and stock pairs.
    """

    def backtest_menu() -> str:
        """
        Shows backtest options and returns user choice.
        Returns:
        str: User's menu choice.
        """
        blue_bold_print("1: Visualise Spread")
        blue_bold_print("2: Visualise Z-Scored Spread")
        blue_bold_print("3: Visualise Returns")
        return input("Please select an option or type 'b' to return to the main menu: ")

    if not pair:
        blue_bold_print("Please enter the stock ticker you would like to backtest in the format stock_1, stock_2:")
        pair_input = input()
        pair_list = [pair.strip() for pair in pair_input.split(',')]
        strategy_info = collect_metrics_for_pair(pair_list[0], pair_list[1])

    else:
        strategy_info = collect_metrics_for_pair(pair[0], pair[1])

    while True:
        try:
            choice = backtest_menu()
            if choice not in ["1", "2", "3", "b"]:
                raise ValueError
            elif choice == "1":
                blue_bold_print("You have selected to visualise the spread.")
                spread_visualisation(strategy_info)
            elif choice == "2":
                blue_bold_print("You have selected to visualise the Z-scored spread.")
                zscored_spread(strategy_info)
            elif choice == "3":
                blue_bold_print("You have selected to visualise the returns.")
                blue_bold_print("Specify a take profit and stop loss percentage in the format 0.05, 0.05:")
                tp_sl = input()
                tp, sl = tp_sl.split(',')
                tp, sl = float(tp.strip()), float(sl.strip())
                visualise_returns(strategy_info, tp, sl)
            elif choice == 'b':
                break
        except Exception as e:
            print(e)
