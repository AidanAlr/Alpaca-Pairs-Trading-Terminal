import os
import sys

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from Trading.AlpacaFunctions import Alpaca


def execute_algo(tp, sl):
    alpaca = Alpaca()
    alpaca.use_live_tp_sl(tp, sl)


execute_algo(5, 5)
