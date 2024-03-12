import yfinance as yf
import os
import logging
import pandas as pd
from datetime import datetime


class StockTradingBot:
    """
    A class representing a stock trading bot.

    Attributes:
        symbol (str): The symbol of the stock.
        short_window (int): The window size for the short-term moving average.
        long_window (int): The window size for the long-term moving average.
        initial_cash (float): The initial amount of cash available for trading.
        shares_amount (int): The number of shares to trade.
        cash (float): The current amount of cash available for trading.
        stock_balance (int): The current number of shares held.
        history (list): A list of trading history.
        logger (Logger): The logger object for logging errors.

    Methods:

        get_stock_data(start_date, end_date):
            Retrieves stock data for a given symbol and date range.

        calculate_sma(data, window):
            Calculate the Simple Moving Average (SMA) for a given data set.

        update_balance(price, amount, operation):
            Updates the balance of cash and stock based on the given price, amount, and operation.

        buy(price, amount):
            Buys a specified amount of shares at the given price.

        sell(price, amount):
            Sells a specified amount of shares at the given price.

        execute_strategy(data):
            Executes the trading strategy based on the given stock data.

        run():
            Runs the stock trading bot by fetching stock data, executing the strategy, and displaying the trading history and portfolio summary.

        display_portfolio(data):
            Displays the portfolio summary including cash, stock balance, and portfolio value.

        display_history():
            Displays the trading history.
    """

    def __init__(self, symbol, initial_cash, shares_amount, start_date, end_date):
        self.symbol = symbol
        self.cash = initial_cash
        self.stock_balance = 0
        self.history = []
        self.shares_amount = shares_amount
        self.logger = logging.getLogger(__name__)
        self.start_date = start_date
        self.end_date = end_date

    def get_stock_data(self, start_date, end_date):
        """
        Retrieves stock data for a given symbol and date range.

        Args:
            start_date (str): The start date of the data range in the format 'YYYY-MM-DD'.
            end_date (str): The end date of the data range in the format 'YYYY-MM-DD'.

        Returns:
            pandas.DataFrame or None: The stock data as a pandas DataFrame if successful, None otherwise.
        """
        try:
            data = yf.download(self.symbol, start=start_date, end=end_date)
            return data
        except Exception as e:
            self.logger.error(f"Error downloading stock data: {e}")
            return None

    def calculate_sma(self, data, window):
        """
        Calculate the Simple Moving Average (SMA) for a given data set.

        Parameters:
        - data: pandas DataFrame containing the data set.
        - window: integer representing the window size for the moving average calculation.

        Returns:
        - pandas Series representing the SMA values.
        """
        return data["Close"].rolling(window=window).mean()

    def update_balance(self, price, amount, operation):
        """
        Updates the balance of cash and stock based on the given price, amount, and operation.

        Args:
            price (float): The price of each share.
            amount (int): The number of shares to buy or sell.
            operation (str): The operation to perform, either "buy" or "sell".

        Raises:
            ValueError: If the operation is not "buy" or "sell".

        Returns:
            None
        """
        if operation == "buy":
            total_cost = price * amount
            if self.cash >= total_cost:
                self.cash -= total_cost
                self.stock_balance += amount
                self.append_history(operation, price, amount)
            else:
                self.append_history(operation, price, amount, insufficent_funds=True)
        elif operation == "sell":
            if self.stock_balance >= amount:
                total_sale = price * amount
                self.cash += total_sale
                self.stock_balance -= amount
                self.append_history(operation, price, amount)
            else:
                self.append_history(operation, price, amount, insufficent_funds=True)
        else:
            raise ValueError("Invalid operation. Operation must be 'buy' or 'sell'.")

    def buy(self, price, amount):
        self.update_balance(price, amount, "buy")

    def sell(self, price, amount):
        self.update_balance(price, amount, "sell")

    def execute_strategy(self, data):
        """
        Executes the trading strategy based on the given stock data.

        Args:
            data (pandas.DataFrame): The stock data as a pandas DataFrame.

        Returns:
            None
        """
        # This method should be implemented in the subclasses
        pass

    def run(self):
        """
        Runs the stock trading bot by fetching stock data, executing the strategy,
        and displaying the trading history and portfolio summary.

        Returns:
            None
        """
        data = self.get_stock_data("2000-01-01", "2024-01-01")

        self.execute_strategy(data)

        portfolio = self.get_portfolio(data)
        portfolio["history"] = self.history
        return portfolio

    def get_portfolio(self, data):
        """
        Get the portfolio including cash, stock balance, and portfolio value.

        Args:
            data (pandas.DataFrame): The stock data as a pandas DataFrame.

        Returns:
            None
        """
        close_price = data["Close"].iloc[-1]
        portfolio_value = self.cash + self.stock_balance * close_price
        portfolio = {
            "cash": self.cash,
            "stock_balance": self.stock_balance,
            "portfolio_value": portfolio_value,
        }
        return portfolio

    def display_history(self):
        """
        Displays the trading history.

        Returns:
            None
        """
        print(f"Trading History:")
        for item in self.history:
            print(item)

    def append_history(self, operation, price, amount, insufficent_funds=False):
        if insufficent_funds:
            history = {
                "operation": operation,
                "price": price,
                "amount": amount,
                "timestamp": datetime.now(),
                "insufficent_funds": insufficent_funds,
            }
        else:
            history = {
                "operation": operation,
                "price": price,
                "amount": amount,
                "timestamp": datetime.now(),
                "insufficent_funds": insufficent_funds,
            }
        self.history.append(history)
