# kalman_qstrader_backtest.py

import click

import datetime
from qstrader import settings
from qstrader.compat import queue
from qstrader.price_parser import PriceParser
from qstrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from qstrader.position_sizer.naive import NaivePositionSizer
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.compliance.example import ExampleCompliance
from qstrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
# from qstrader.statistics.tearsheet import TearsheetStatistics


# THIS IS NEEDED FOR QSTrader EXAMPLE CODE TO PRODUCE THE TEARSHEET
import matplotlib
matplotlib.use('TkAgg')

from qstrader.strategy.base import AbstractStrategy
from qstrader.event import SignalEvent, EventType
from qstrader.trading_session import TradingSession


# from qstrader.strategy import Strategies, DisplayStrategy
# # from qstrader.strategy.base import AbstractStrategy
from qstrader.strategy.base import Strategies #,  DisplayStrategy
#
#
# from qstrader.trading_session.backtest import Backtest
# # from qstrader.trading_session import TradingSession



from kalman_qstrader_strategy import KalmanPairsTradingStrategy


def run(config, testing, tickers, filename):

    title = ['Kalman Pairs Trade Example']

    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2014, 1, 1)

    # Set up variables needed for backtest
    events_queue = queue.Queue()
    csv_dir = config.CSV_DATA_DIR
    initial_equity = PriceParser.parse(100000.00)

    # Use Yahoo Daily Price Handler
    price_handler = YahooDailyCsvBarPriceHandler(
        csv_dir, events_queue, tickers
    )

    # Use the KalmanPairsTrading Strategy
    strategy = KalmanPairsTradingStrategy(tickers, events_queue)
    # strategy = Strategies(strategy, DisplayStrategy())
    strategy = Strategies(strategy)
    # strategy = AbstractStrategy(strategy)

    # Use the Naive Position Sizer (suggested quantities are followed)
    position_sizer = NaivePositionSizer()

    # Use an example Risk Manager
    risk_manager = ExampleRiskManager()

    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler(
        initial_equity, events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the ExampleCompliance component
    compliance = ExampleCompliance(config)

    # Use a simulated IB Execution Handler
    execution_handler = IBSimulatedExecutionHandler(
        events_queue, price_handler, compliance
    )

    # Use the default Statistics
    # statistics = TearsheetStatistics(
    #     config, portfolio_handler, title=""
    # )

    # Set up the backtest
    # backtest = Backtest(
    #     price_handler, strategy,
    #     portfolio_handler, execution_handler,
    #     position_sizer, risk_manager,
    #     statistics, initial_equity
    # )
    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, title=title
    )
    # backtest = TradingSession(
    #     price_handler, strategy,
    #     portfolio_handler, execution_handler,
    #     position_sizer, risk_manager,
    #     statistics, initial_equity
    # )

    # results = backtest.simulate_trading(testing=testing)
    # statistics.save(filename)
    # return results

    results = backtest.start_trading(testing=testing)
    return results


@click.command()
@click.option('--config', default=settings.DEFAULT_CONFIG_FILENAME, help='Config filename')
@click.option('--testing/--no-testing', default=False, help='Enable testing mode')
@click.option('--tickers', default='SP500TR', help='Tickers (use comma)')
@click.option('--filename', default='', help='Pickle (.pkl) statistics filename')
def main(config, testing, tickers, filename):
    tickers = tickers.split(",")
    config = settings.from_file(config, testing)
    run(config, testing, tickers, filename)


if __name__ == "__main__":
    main()