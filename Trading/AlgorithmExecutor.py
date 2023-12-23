from AlpacaFunctions import Alpaca


def execute_algo(tp, sl):
    alpaca = Alpaca()
    alpaca.use_live_tp_sl(5, 5)


execute_algo(5, 5)
