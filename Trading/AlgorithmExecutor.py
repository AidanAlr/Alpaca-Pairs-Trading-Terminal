import sys

from AlpacaFunctions import Alpaca

sys.path.append("/Users/aidanalrawi/PycharmProjects/Pairs-Trading-Algorithm")


def execute_algo(tp, sl):
    alpaca = Alpaca()
    alpaca.use_live_tp_sl(5, 5)


execute_algo(5, 5)
