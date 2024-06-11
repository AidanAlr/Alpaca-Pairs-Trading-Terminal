<div align="center">
<h1 align="center">
<br> Alpaca Stock Terminal CLI with Pairs Trading Algorithm</h1>
<h3>◦ Built on the official ALPACA API.</h3>

<p align="center">
<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat-square&logo=SciPy&logoColor=white" alt="SciPy" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat-square&logo=NumPy&logoColor=white" alt="NumPy" />
</p>
<img src="https://img.shields.io/github/license/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>


## 📍 Overview
This command line interface allows users to interact with their alpaca brokerage account through the terminal.
Features include view current profits and positions, get asset price quotes, execute trades, run analyses, backtest strategies, and implement a pairs trading strategy all from the command line.

---

## Demo of interactive menu
https://private-user-images.githubusercontent.com/112656616/300945934-8416627c-4eca-48e3-b22e-599934ea1b14.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDY2NDUzODMsIm5iZiI6MTcwNjY0NTA4MywicGF0aCI6Ii8xMTI2NTY2MTYvMzAwOTQ1OTM0LTg0MTY2MjdjLTRlY2EtNDhlMy1iMjJlLTU5OTkzNGVhMWIxNC5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTMwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEzMFQyMDA0NDNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03MDY1Y2Y3Mzk3OTc4ZmU4MzBjYTQ3MmYzZGRlY2ZjZGM2Yzk3MTg2OWIzMmY4YWE4ZDc4MGNiY2YxODViY2JlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.TDAbEMsk63y7zbIQVI1LQdjiZd_5YqkpmNl_3MQ91Ys


---

## 📦 Features

► Analysis

Conduct the analysis required to find a suitable pair for statistical arbitrage. Submit a CSV file of stock tickers and the program will download the stock data from the last year and check the correlation between all assets. If a pair has a sufficiently high correlation, it is placed through ADF test to check the stationarity of the time series and cointegration tests for the suitability of the pair. Once a suitable pair is chosen, we use a  60-day rolling regression on the asset prices allowing us to generate the hedge ratio; we then analyse the relative spread between assets. When the spread exceeds a certain boundary, we will buy one asset and short the other expecting the spread to retract.

You will be presented with the option to backtest the strategy as well.

► Backtest strategy

Dashboard that generates graphic representations of spread, zscored spread and strategy return.
Allows you to test different strategies by adjusting take profits and stop loss.

► Execute Pairs Trading Strategy

Once you have chosen a pair execute and manage a pairs trading strategy directly from your terminal.

► View current positions with profit and loss

Dashboard for viewing all important metrics about current positions.

► Manual Trade

Option to conduct a manual trade, market or limit order.

► Get Quote

Option to conduct get the market price of an asset.


► Close All Positions 

Option to quickly exit all positions.

---

### 🔧 Installation

1. Clone the Pairs-Trading-Algorithm repository:
```sh
git clone https://github.com/AidanAlr/Pairs-Trading-Algorithm
```

2. Change to the project directory:
```sh
cd Pairs-trading-Algorithm
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```
```sh
add account details to trading .FAKENV and change to .env
```

### 🤖 Running Program

Change to the directory containing the cloned repository.
Open the terminal in this folder.

Enter to see a list of command line arguments:
```sh
python terminal.py -h
```

To interact with the terminal through an interactive menu:
```sh
python terminal.py -im
```
---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Report Issues](https://github.com/AidanAlr/Pairs-Trading-Algorithm/issues)**: Submit bugs found or log feature requests for AIDANALR.

---

[**Return**](#Top)

---

