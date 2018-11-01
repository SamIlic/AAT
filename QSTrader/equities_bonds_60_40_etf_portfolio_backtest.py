"""
python equities_bonds_60_40_etf_portfolio_backtest.py
"""

# # THIS IS NEEDED FOR QSTrader EXAMPLE CODE TO PRODUCE THE TEARSHEET
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt

import datetime

from qstrader import settings
from monthly_rebalance_run import run_monthly_rebalance

if __name__ == "__main__": 
    tickers = ["SPY", "AGG"] 
    ticker_weights = {
        "SPY": 0.6,
        "AGG": 0.4, 
    }

    run_monthly_rebalance(
        tickers, ticker_weights,
        title="US Equities/Bonds 60/40 Mix ETF Strategy",
        start_date=datetime.datetime(2003, 9, 29),
        end_date=datetime.datetime(2016, 10, 12),
        initial_equity=500000.00
    )
