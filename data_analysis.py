import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import openpyxl as xl
import numpy as np

location = 'C:\\Users\\aidan\\PycharmProjects\\New Algo\\Combined Data\\Combined_excel.xlsx'

def run_correlation():
    df = pd.read_excel(location)
    df = df.drop('Date', axis=1)
    corr_matrix = df.corr()
    print('Correlation Matrix generated from your stock picks: ')
    corr_pairs = corr_matrix.unstack().drop_duplicates().sort_values(kind='quicksort')
    np.fill_diagonal(corr_matrix.values, np.nan)
    print(corr_matrix)
    print('\n')

    # Eliminating self corr
    corr_pairs = corr_pairs[corr_pairs < 1]
    print('Sorted Pairs: ')
    print(corr_pairs)

    #Heatmap
    plt.title("Correlation Matrix Created From Chosen Stocks")
    plt.get_cmap('Greens')
    sn.heatmap(corr_matrix, annot=True, cmap='Greens')
    plt.show()
    plt.savefig("Correlation Matrix Generated.png")


run_correlation()

#corr_matrix.to_excel('Correlation.xlsx')
##ws1 = wb.worksheets[0]
#max_rows = ws1.max_row
#max_columns = ws1.max_column
#top_row = 'A' + str(max_columns)
#for row in ws1[f'A1:{top_row}']:
    #for cell in row:
     #   cell.value = None
#wb.save('Correlation.xlsx')