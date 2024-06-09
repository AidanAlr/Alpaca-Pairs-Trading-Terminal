import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


from utils.formatting_and_logs import blue_bold_print

mpl.use("tkagg")


def get_tickers_from_collected_data_df(df) -> (str, str):
    tickers = []
    for column in df.columns:
        if column.endswith("_forward_return"):
            tickers.append(column.split("_")[0])
    return tickers[0], tickers[1]


def spread_visualisation(df):
    blue_bold_print("You have selected to visualise the spread.")
    stock_1, stock_2 = get_tickers_from_collected_data_df(df)
    hedge_ratio = round(df["hedge_ratio"].iloc[-1], 2)
    plt.title(f"{stock_1}-{hedge_ratio}*{stock_2}")
    df["spread"].plot(figsize=(16, 4), color="red")
    plt.show()


def zscored_spread(df):
    blue_bold_print("You have selected to visualise the Z-scored spread.")
    # Plot Z-scored spread
    df["z_score"].plot(figsize=(16, 4), color="orange")
    plt.title("Z-scored Spread")
    plt.axhline(1, color="k")
    plt.axhline(-1, color="k")
    plt.show()


def visualise_returns(strategy_info_df, tp, sl):
    stock_1, stock_2 = get_tickers_from_collected_data_df(strategy_info_df)
    strategy_info_df = strategy_info_df.dropna()
    strategy_info_df["combined_return"] = (
        strategy_info_df[f"{stock_1}_return"]
        + strategy_info_df[f"{stock_2}_return"] * strategy_info_df["hedge_ratio"]
    )

    def check_strategy_signal(df):
        if df["combined_return"] > tp or df["z_score"] < -1:
            return 1
        elif df["combined_return"] < sl or df["z_score"] > 1:
            return -1
        else:
            return 0

    # trading Signal
    strategy_info_df["signal"] = strategy_info_df.apply(check_strategy_signal, axis=1)
    strategy_info_df["strategy_return"] = (
        strategy_info_df[f"{stock_1}_forward_return"] * strategy_info_df["signal"]
        + strategy_info_df[f"{stock_2}_forward_return"]
        * strategy_info_df["signal"]
        * -strategy_info_df["hedge_ratio"]
    )

    portfolios_cumulative_return = np.exp(
        np.log1p(strategy_info_df["strategy_return"]).cumsum()
    )
    portfolios_cumulative_return.plot(figsize=(16, 6), color="red")
    plt.title("Strategy Cumulative Returns")
    plt.ylabel("Return")
    plt.show()
