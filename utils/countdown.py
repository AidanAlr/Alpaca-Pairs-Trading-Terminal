import sys
import time


def countdown(seconds):
    """ Prints a countdown to the console. """
    while seconds:
        sys.stdout.write("\r" + str(seconds) + ' ')
        time.sleep(1)
        seconds -= 1
        sys.stdout.flush()