import os
import sys

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from trading.alpaca_functions import Alpaca
from utils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print, emphasis_bold_red_print
from executors import analysis_executor
from executors import alpaca_executor


def main_menu(alpaca: Alpaca) -> str:
    """ Displays the main menu and returns the user's choice. """
    sys.stdout.write("\n")
    emphasis_bold_red_print("Main Menu | " + "Alpaca Balance: $" + str(alpaca.account.buying_power))
    blue_bold_print("1: Current Positions - Live Portfolio")
    blue_bold_print("2: Run analysis - Find Suitable Pair")
    blue_bold_print("3: Execute pairs trading strategy")
    blue_bold_print("4: Backtest Strategy")
    blue_bold_print("5: Manual Trade")
    blue_bold_print("6: Get Price Quote")
    blue_bold_print("7: Close All Positions")
    choice = input("Please select an option: ")
    return choice


def main():
    """ Main function for the CLI controller. """
    alpaca_connection = Alpaca()
    while True:
        try:
            choice = main_menu(alpaca=alpaca_connection)
            match choice:
                case "1":
                    alpaca_executor.live_position_menu(alpaca_connection)
                case "2":
                    analysis_executor.run_analysis()
                case "3":
                    analysis_executor.execute_pairs_strategy([])
                case "4":
                    analysis_executor.backtest_strategy([])
                case "5":
                    alpaca_executor.manual_trade_menu(alpaca_connection)
                case "6":
                    alpaca_executor.quote_menu()
                case "7":
                    alpaca_connection.close_all_positions()
                case _:  # Default case
                    raise ValueError
        except ValueError:
            red_bold_print("Invalid input")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
