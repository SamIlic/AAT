# ensemble_prediction.py

"""
- This script will apply 3 ensemble methods to predict the daily Amazon 
    returns using the prior 3 days as lagged returns
- Ensemble Methods: Boosting, Bagging, Random Forests
- We will create a plot of MSE for each of the enseble methods

"""

import datetime # timestamps

import matplotlib.pyplot as plt # data analysis and plottnig
import numpy as np
import pandas as pd
import seaborn as sns

import pandas_datareader.data as web # read from yahoo finance

import sklearn # ML
from sklearn.ensemble import (
    BaggingRegressor, RandomForestRegressor, AdaBoostRegressor
)
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeRegressor

"""
This creates a pandas DataFrame that stores
the percentage returns of the adjusted closing
value of a stock obtained from Yahoo Finance,
along with a number of lagged returns from the
prior trading days (lags defaults to 3 days).
Trading volume, as well as the Direction from
the previous day, are also included.
- Creates a DF containing 3 days of lagged returns from Yahoo Finance
"""
def create_lagged_series(symbol, start_date, end_date, lags=3):
    
    print('~~~~~~~~~~~~~~~~~~~~~~~')
    print('Creating Lagged Series')
    print('~~~~~~~~~~~~~~~~~~~~~~~')
    # Obtain stock information from Yahoo Finance
    ts = web.DataReader(
        symbol, "yahoo", start_date, end_date
    )

    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag["Today"] = ts["Adj Close"]
    tslag["Volume"] = ts["Volume"]

    # Create the shifted lag series of
    # prior trading period close values
    for i in range(0, lags):
        tslag["Lag%s" % str(i + 1)] = ts["Adj Close"].shift(i + 1)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Volume"] = tslag["Volume"]
    tsret["Today"] = tslag["Today"].pct_change() * 100.0

    # Create the lagged percentage returns columns
    for i in range(0, lags):
        tsret["Lag%s" % str(i + 1)] = tslag[
            "Lag%s" % str(i + 1)
            ].pct_change() * 100.0
    tsret = tsret[tsret.index >= start_date]
    return tsret

"""
MAIN 
- parameters are set for calculations
- Download amazon data, convert to return series, call create lagged series
- Drop missing values, scale data between -1n1 to make comparisons easier
- Split data into Training(70) & Test(30)
- Create Numpy array to store estimators at each steo as well as its MSE for each ensemble method

- Ensemble Methods
    - Bagging
        - 
"""
if __name__ == "__main__":
    # Set the random seed, number of estimators
    # and the "step factor" used to plot the graph of MSE
    # for each method
    random_state = 42  # Seed
    n_jobs = 1  # Parallelisation factor for bagging, random forests (controls the number of processor cores used)
    n_estimators = 1000 # total number of estimators ot use in the MSE graph
    step_factor = 10 # controls cranularity of calculation by stepping through the number of estimators
    axis_step = int(n_estimators / step_factor) # 1000/10 = 100 separate calculations will be performed for each of the 3 ensebmle methods

    # Download ten years worth of Amazon
    # adjusted closing prices
    start = datetime.datetime(2006, 1, 1)
    end = datetime.datetime(2015, 12, 31)
    amzn = create_lagged_series("AMZN", start, end, lags=3)
    amzn.dropna(inplace=True)

    # Use the first three daily lags of AMZN closing prices
    # and scale the data to lie within -1 and +1 for comparison
    X = amzn[["Lag1", "Lag2", "Lag3"]]
    y = amzn["Today"]
    X = scale(X)
    y = scale(y)

    # Use the training-testing split with 70% of data in the
    # training data with the remaining 30% of data in the testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )

    # Pre-create the arrays which will contain the MSE for
    # each particular ensemble method
    estimators = np.zeros(axis_step)
    bagging_mse = np.zeros(axis_step)
    rf_mse = np.zeros(axis_step)
    boosting_mse = np.zeros(axis_step)

    """
    Bagging
    """
    # Estimate the Bagging MSE over the full number
    # of estimators, across a step size ("step_factor")
    for i in range(0, axis_step): # 0-100
        print("Bagging Estimator: %d of %d..." % (
            step_factor * (i + 1), n_estimators)
              )
        bagging = BaggingRegressor(
            DecisionTreeRegressor(),
            n_estimators=step_factor * (i + 1),
            n_jobs=n_jobs,
            random_state=random_state
        )
        bagging.fit(X_train, y_train)
        mse = mean_squared_error(y_test, bagging.predict(X_test))
        estimators[i] = step_factor * (i + 1)
        bagging_mse[i] = mse

    """
    Random Forest
    """
    # Estimate the Random Forest MSE over the full number
    # of estimators, across a step size ("step_factor")
    for i in range(0, axis_step):
        print("Random Forest Estimator: %d of %d..." % (
            step_factor * (i + 1), n_estimators)
              )
        rf = RandomForestRegressor(
            n_estimators=step_factor * (i + 1),
            n_jobs=n_jobs,
            random_state=random_state
        )
        rf.fit(X_train, y_train)
        mse = mean_squared_error(y_test, rf.predict(X_test))
        estimators[i] = step_factor * (i + 1)
        rf_mse[i] = mse

    """
    Boosting
    """
    # Estimate the AdaBoost MSE over the full number
    # of estimators, across a step size ("step_factor")
    for i in range(0, axis_step):
        print("Boosting Estimator: %d of %d..." % (
            step_factor * (i + 1), n_estimators)
              )
        boosting = AdaBoostRegressor(
            DecisionTreeRegressor(),
            n_estimators=step_factor * (i + 1),
            random_state=random_state,
            learning_rate=0.01
        )
        boosting.fit(X_train, y_train)
        mse = mean_squared_error(y_test, boosting.predict(X_test))
        estimators[i] = step_factor * (i + 1)
        boosting_mse[i] = mse

    # Plot the chart of MSE versus number of estimators
    plt.figure(figsize=(8, 8))
    plt.title('Bagging, Random Forest and Boosting comparison')
    plt.plot(estimators, bagging_mse, 'b-', color="black", label='Bagging')
    plt.plot(estimators, rf_mse, 'b-', color="blue", label='Random Forest')
    plt.plot(estimators, boosting_mse, 'b-', color="red", label='AdaBoost')
    plt.legend(loc='upper right')
    plt.xlabel('Estimators')
    plt.ylabel('Mean Squared Error')
    plt.show()