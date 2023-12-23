
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# If the script is not in the root directory, navigate to the root directory
root_dir = os.path.dirname(current_dir)
# Append the root directory to sys.path so that modules can be imported
sys.path.append(root_dir)



from Analysis.StockData import StockData

SYMBOLS_LIST = ['XOM', 'CVX', 'BP', 'COP', 'PXD', 'EOG', 'APA', 'OXY', 'MPC', 'SLB', 'HAL', 'KMI', 'PBR', 'SU', 'ENB',
                'EPD', 'EQT', 'BHP',
                'FCX', 'NEM', 'GOLD', 'WPM', 'AGI', 'TECK', 'SBSW', 'CF', 'ADM', 'MOS', 'FMC', 'LIN', 'NUE', 'RGLD',
                'WY', 'PAA', 'ET',
                'MPLX',
                'WMB', 'X', 'AA', 'CMP', 'IP', 'PKG', 'PPG']


def run():
    stock_data = StockData(asset_list=SYMBOLS_LIST)
    print(stock_data.co_int_correlation_combined_df)


if __name__ == '__main__':
    run()
