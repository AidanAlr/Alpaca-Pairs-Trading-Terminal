import unittest
import numpy as np
import pandas as pd
from analysis.statistical_methods import collect_metrics_for_pair
import warnings

no_df_result = "result is not a DataFrame"

class TestCollectMetricsForPair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stock_1 = 'AAPL'
        cls.stock_2 = 'MSFT'
        cls.metrics = collect_metrics_for_pair('AAPL', 'MSFT')
        warnings.filterwarnings("ignore")

    def test_download_stock_data(self):
        assert isinstance(self.metrics, pd.DataFrame)
        assert not self.metrics.empty, "DataFrame download empty: Failed to download stock data"

    def test_calculate_return(self):
        assert any('forward_return' in column for column in self.metrics.columns), "forward_return not found in columns"
        assert any('return' in column for column in self.metrics.columns), "return not found in columns"

    def test_calculate_hedge_ratio(self):
        assert 'hedge_ratio' in self.metrics.columns, "hedge_ratio not found in columns"

    def test_missing_stock_data(self):
        assert isinstance(self.metrics, pd.DataFrame), no_df_result
        assert not self.metrics.isnull().values.any(), "result contains NaN values"

    def test_infinite_hedge_ratio(self):
        assert isinstance(self.metrics, pd.DataFrame), no_df_result
        assert not self.metrics.isin([np.inf, -np.inf, np.nan]).values.any(), "result contains infinite or NaN values"

    def test_calculate_spread(self):
        assert isinstance(self.metrics, pd.DataFrame), no_df_result
        assert 'spread' in self.metrics.columns, "spread not found in columns"

    def test_calculate_rolling_correlation(self):
        assert isinstance(self.metrics, pd.DataFrame), no_df_result
        assert 'roll_corr' in self.metrics.columns, "roll_corr not found in columns"

    def test_calculate_z_score(self):
        assert isinstance(self.metrics, pd.DataFrame), no_df_result
        assert 'z_score' in self.metrics.columns, "z_score not found in columns"


if __name__ == '__main__':
    unittest.main()
