<div align="center">
<h1 align="center">
<img src="" width="100" />
<br> Stock Analysis Terminal with Pairs Trading Algorithm</h1>
<h3>◦ Developed to interact with the ALPACA API with the software and tools below.</h3>

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

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 Repository Structure](#-repository-structure)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running Pairs-Trading-Algorithm](#-running-Pairs-Trading-Algorithm)
- [🤝 Contributing](#-contributing)

---


## 📍 Overview
This command line interface (CLI) application, developed to interact with the Alpaca API (stock brokerage), allows users to manage and view positions, execute trades, run analyses, backtest strategies, and implement a pairs trading strategy. 

The code is organised in a modular format, with analysis and trading functions in separate directories. Executor files import functions and methods from these classes.

---


## Demo
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


## 📂 Repository Structure

```sh
└── Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/
    ├── requirements.txt
    ├── analysis/
    │   ├── DATES.py
    │   ├── errors.py
    │   ├── statistical_methods.py
    │   ├── stock_data.py
    │   └── visualisation.py
    ├── executors/
    │   ├── alpaca_executor.py
    │   ├── analysis_executor.py
    │   └── cli_controller.py
    ├── trading/
    │   ├── account_details.py
    │   └── alpaca_functions.py
    └── utils/
        ├── ProgressBar.py
        ├── countdown.py
        ├── formatting_and_logs.py
        └── my_timer.py

```


---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                                                                               | Summary       |
| ---                                                                                                | ---           |
| [requirements.txt](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/requirements.txt) | ► Requirements needed to run program, use "pip install -r requirements.txt" |

</details>

<details closed><summary>Analysis</summary>

| File                                                                                                                                                 | Summary                   |
| ---                                                                                                                                                  | ---                       |
| [statistical_methods.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/analysis/statistical_methods.py) | ► Functions to visualise important metrics |
| [visualisation.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/analysis/visualisation.py)             | ► Functions to visualise important metrics |
| [DATES.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/analysis/DATES.py)                             | ► StockData class and methods |
| [errors.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/analysis/errors.py)                           | ► Enum for dates |
| [stock_data.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/analysis/stock_data.py)                   | ► Functions performing statisticaly analysis on StockData |


</details>

<details closed><summary>Tests</summary>

| File                                                                                                 | Summary       |
| ---                                                                                                  | ---           |
| [test_alpaca.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Tests/test_alpaca.py) | ► Testing the Alpaca Functions |

</details>

<details closed><summary>Executors</summary>

| File                                                                                                                                              | Summary                   |
| ---                                                                                                                                               | ---                       |
| [cli_controller.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/executors/cli_controller.py)       | ► Main entry point into program - main_menu handler |
| [alpaca_executor.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/executors/alpaca_executor.py)     | ► Executor for trading functions |
| [analysis_executor.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/executors/analysis_executor.py) | ► Executor for analysis functions |

</details>

<details closed><summary>Aidanutils</summary>
| File                                                                                                                                              | Summary                   |
| ---                                                                                                                                               | ---                       |
| [my_timer.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/utils/my_timer.py)                       | ► Timer decorator for functions |
| [formatting_and_logs.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/utils/formatting_and_logs.py) | ► Log helper |
| [ProgressBar.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/utils/ProgressBar.py)                 | ► Progress bar printer |
| [countdown.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/utils/countdown.py)                     | ► Countdown function | 

</details>

<details closed><summary>Trading</summary>

| File                                                                                                                                          | Summary                   |
| ---                                                                                                                                           | ---                       |
| [alpaca_functions.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/trading/alpaca_functions.py) | ► Interact with ALPACA API |
| [account_details.py](https://github.com/AidanAlr/Stock-Analysis-Terminal-with-Pairs-Trading-Algorithm/blob/main/trading/account_details.py)   | ► Account details enum for user input |

</details>

---

## 🚀 Getting Started

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
add account details to trading/account_details.py
```

### 🤖 Running Program
1. Change to the Executors directory:
```sh
cd Pairs-trading-Algorithm/executors
```
```sh
python -m cli_controller
```


---
### 🤖 Running Program with docker
This program can also be run as a container using the provided dockerfile. Simply create a new image using this dockerfile and run the container.


---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Report Issues](https://github.com/AidanAlr/Pairs-Trading-Algorithm/issues)**: Submit bugs found or log feature requests for AIDANALR.



---

[**Return**](#Top)

---

