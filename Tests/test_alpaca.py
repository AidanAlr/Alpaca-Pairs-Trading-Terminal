import sys
import unittest
from Trading.AlpacaFunctions import Alpaca
sys.path.append("/Users/aidanalrawi/PycharmProjects/Pairs-Trading-Algorithm")


class TestAlpacaFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This will only run once when the TestAlpacaFunctions class is created"""
        # Create an instance of Alpaca
        cls.alpaca = Alpaca()

    def test_connection(self):
        self.assertTrue(self.alpaca.connected, 'Failed to connect to alpaca')




