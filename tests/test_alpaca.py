import os
import sys
import unittest

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# If the script is not in the root directory, navigate to the root directory
root_dir = os.path.dirname(current_dir)
# Append the root directory to sys.path so that modules can be imported
sys.path.append(root_dir)

from trading.alpaca_functions import Alpaca


class TestAlpacaFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This will only run once when the TestAlpacaFunctions class is created"""
        # Create an instance of Alpaca
        cls.alpaca = Alpaca()

    def test_connection(self):
        self.assertTrue(self.alpaca.connected, 'Failed to connect to alpaca')
