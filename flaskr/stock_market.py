# Raw Package
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr

# Market Data
import yfinance as yf

# Graphing / Visualization
import plotly.graph_objs as go


def get_stock_data(stock, period, interval):
    yf.pdr_override()
    # Import the data frame (df) from yahoo finance using the specified stock as the ticker symbol
    df = yf.download(tickers=stock, period="1d", interval="60m")

    # print the data we have requested
    return df
