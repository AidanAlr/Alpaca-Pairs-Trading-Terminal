from ..Analysis.StockData import StockData

SYMBOLS_LIST = ['XOM', 'CVX', 'BP', 'COP', 'PXD', 'EOG', 'APA', 'OXY', 'MPC', 'SLB', 'HAL', 'KMI', 'PBR', 'SU', 'ENB', 'EPD', 'EQT', 'BHP',
                'FCX', 'NEM', 'GOLD', 'WPM', 'AGI', 'TECK', 'SBSW', 'CF', 'ADM', 'MOS', 'FMC', 'LIN', 'NUE', 'RGLD', 'WY', 'PAA', 'ET',
                'MPLX',
                'WMB', 'X', 'AA', 'CMP', 'IP', 'PKG', 'PPG']


def run():
    stock_data = StockData(asset_list=SYMBOLS_LIST)
    print(stock_data.co_int_correlation_combined_df)


if __name__ == '__main__':
    run()
