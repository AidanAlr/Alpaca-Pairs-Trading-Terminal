<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>PAIRS-TRADING-ALGORITHM</h1>
<h3>◦ Statistical Arbitrage Trading Algorithm</h3>
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
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running Pairs-Trading-Algorithm](#-running-Pairs-Trading-Algorithm)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

► This Algorithm is separated into Analysis and Trading Functions.
Analysis contains the statistical methods required to implement a statistical arbitrage strategy.
Trading contains the methods that interact with the Alpaca API to execute the strategy.  
The algorithm is configured to use my ALPACA paper account API key and secret.



---

## 📦 Features

► Analysis


---


## 📂 Repository Structure

```sh
└── Pairs-Trading-Algorithm/
    ├── AidanUtils/
    │   ├── MyTimer.py
    │   ├── ProgressBar.py
    ├── Analysis/
    │   ├── Dates.py
    │   ├── StatisticalMethods.py
    │   ├── StockData.py
    │   ├── Visualisation.py
    ├── Executors/
    │   ├── AlgorithmExecutor.py
    │   └── AnalysisExecutor.py
    ├── Tests/
    │   └── test_alpaca.py
    ├── Trading/
    │   ├── AlpacaFunctions.py
    └── requirements.txt

```

---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                                                                               | Summary       |
| ---                                                                                                | ---           |
| [requirements.txt](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/requirements.txt) | ► INSERT-TEXT |

</details>

<details closed><summary>Analysis</summary>

| File                                                                                                                  | Summary       |
| ---                                                                                                                   | ---           |
| [Visualisation.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/Visualisation.py)           | ► INSERT-TEXT |
| [StockData.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/StockData.py)                   | ► INSERT-TEXT |
| [Dates.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/Dates.py)                           | ► INSERT-TEXT |
| [StatisticalMethods.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/StatisticalMethods.py) | ► INSERT-TEXT |

</details>

<details closed><summary>Tests</summary>

| File                                                                                                 | Summary       |
| ---                                                                                                  | ---           |
| [test_alpaca.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Tests/test_alpaca.py) | ► INSERT-TEXT |

</details>

<details closed><summary>Executors</summary>

| File                                                                                                                 | Summary       |
| ---                                                                                                                  | ---           |
| [AnalysisExecutor.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Executors/AnalysisExecutor.py)   | ► INSERT-TEXT |
| [AlgorithmExecutor.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Executors/AlgorithmExecutor.py) | ► INSERT-TEXT |

</details>

<details closed><summary>Aidanutils</summary>

| File                                                                                                      | Summary       |
| ---                                                                                                       | ---           |
| [MyTimer.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/AidanUtils/MyTimer.py)         | ► INSERT-TEXT |
| [ProgressBar.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/AidanUtils/ProgressBar.py) | ► INSERT-TEXT |

</details>

<details closed><summary>Trading</summary>

| File                                                                                                           | Summary       |
| ---                                                                                                            | ---           |
| [AlpacaFunctions.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Trading/AlpacaFunctions.py) | ► INSERT-TEXT |

</details>

---

## 🚀 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

`- ℹ️ Dependency 1`

`- ℹ️ Dependency 2`

`- ℹ️ ...`

### 🔧 Installation

1. Clone the Pairs-Trading-Algorithm repository:
```sh
git clone https://github.com/AidanAlr/Pairs-Trading-Algorithm
```

2. Change to the project directory:
```sh
cd Pairs-Trading-Algorithm
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Running Program
1. Change to the Executors directory:
```sh
cd Pairs-Trading-Algorithm/Executors
```


#### Running Analysis

```sh
python -m AnalysisExecutor
```



### 🤖 Running Pairs-Trading-Algorithm

```sh
python -m AlgorithmExecutor
```

### 🧪 Tests

```sh
pytest
```

---


## 🛣 Project Roadmap

> - [X] `ℹ️  Task 1: Implement X`
> - [ ] `ℹ️  Task 2: Implement Y`
> - [ ] `ℹ️ ...`


---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/AidanAlr/Pairs-Trading-Algorithm/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/AidanAlr/Pairs-Trading-Algorithm/issues)**: Submit bugs found or log feature requests for AIDANALR.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License


This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 👏 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#Top)

---

