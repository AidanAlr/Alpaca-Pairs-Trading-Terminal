import sys
import time
from Trading.AlpacaFunctions import AlpacaClient


def pause_algo():
    for remaining in range(5 * 60 * 60, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Paused Algorithm ")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


def execute_algo(tp, sl):
    alpaca = AlpacaClient()
    alpaca.use_live_tp_sl(5,5)


execute_algo(5, 5)
