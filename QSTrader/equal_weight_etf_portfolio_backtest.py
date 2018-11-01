"""
python equal_weight_etf_portfolio_backtest.py
"""

import datetime

# THIS IS NEEDED FOR QSTrader EXAMPLE CODE TO PRODUCE THE TEARSHEET
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt

from qstrader import settings
from monthly_rebalance_run import run_monthly_rebalance


if __name__ == "__main__":
    tickers = [
        "SPY", "IJS", "EFA", "EEM",
        "AGG", "JNK", "DJP", "RWR"
    ]
    ticker_weights = {
        "SPY": 0.125,
        "IJS": 0.125,
        "EFA": 0.125,
        "EEM": 0.125,
        "AGG": 0.125,
        "JNK": 0.125,
        "DJP": 0.125,
        "RWR": 0.125
    }
    run_monthly_rebalance(
        tickers, ticker_weights,
        title="Equal Weight ETF Strategy",
        start_date=datetime.datetime(2007, 12, 4),
        end_date=datetime.datetime(2016, 10, 12),
        initial_equity=500000.00
    )