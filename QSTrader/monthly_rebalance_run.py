# monthly_rebalance_run.py

import calendar
import datetime

# THIS IS NEEDED FOR QSTrader EXAMPLE CODE TO PRODUCE THE TEARSHEET
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from qstrader import settings
from qstrader.strategy.base import AbstractStrategy
# LiquidateRebalancePositionSizer is in rebalance.py
from qstrader.position_sizer.rebalance import LiquidateRebalancePositionSizer
from qstrader.event import SignalEvent, EventType
from qstrader.compat import queue
from qstrader.trading_session import TradingSession

##########################################################################################

"""
A generic strategy that allows monthly rebalancing of a
set of tickers, via 
    1) full liquidation and 
    2) dollar-weighting of new positions

Must be used in conjunction with the
LiquidateRebalancePositionSizer object to work correctly.
"""
class MonthlyLiquidateRebalanceStrategy(AbstractStrategy):
    ### AbstractStrategy Object is in base.py

    def __init__(self, tickers, events_queue):
        self.tickers = tickers
        self.events_queue = events_queue
        self.tickers_invested = self._create_invested_list()

    """
    Determine if the current day is at the end of the month.
    """
    def _end_of_month(self, cur_time):

        cur_day = cur_time.day
        end_day = calendar.monthrange(cur_time.year, cur_time.month)[1]
        return cur_day == end_day

    """
    Create a dictionary with each ticker as a key, with
    a boolean value depending upon whether the ticker has
    been "invested" yet. This is necessary to avoid sending
    a liquidation signal on the first allocation.
    """
    def _create_invested_list(self):
        
        tickers_invested = {ticker: False for ticker in self.tickers}
        return tickers_invested

    """
    For a particular received BarEvent, determine whether
    it is the end of the month (for that bar) and generate
    a liquidation signal, as well as a purchase signal,
    for each ticker.
    """
    def calculate_signals(self, event):

        if (
            event.type in [EventType.BAR, EventType.TICK] and
            self._end_of_month(event.time)
        ):
            ticker = event.ticker
            if self.tickers_invested[ticker]:
                liquidate_signal = SignalEvent(ticker, "EXIT")
                self.events_queue.put(liquidate_signal)
            long_signal = SignalEvent(ticker, "BOT")
            self.events_queue.put(long_signal)
            self.tickers_invested[ticker] = True

"""
"""
def run_monthly_rebalance(
        tickers, ticker_weights, title,
        start_date, end_date, initial_equity
    ):
    testing = False
    config = settings.from_file(
        settings.DEFAULT_CONFIG_FILENAME, testing
    )

    # Use the Monthly Liquidate And Rebalance strategy
    events_queue = queue.Queue()
    strategy = MonthlyLiquidateRebalanceStrategy(
        tickers, events_queue
    )

    # Use the liquidate and rebalance position sizer
    # with prespecified ticker weights
    position_sizer = LiquidateRebalancePositionSizer(
        ticker_weights
    )

    # Set up the backtest
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, position_sizer=position_sizer,
        title=[title], benchmark=tickers[0],
    )
    results = backtest.start_trading(testing=testing)
    return results