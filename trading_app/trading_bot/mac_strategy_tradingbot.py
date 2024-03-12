from trading_app.trading_bot import tradingbot as tb


class MACStrategyTradingBot(tb.StockTradingBot):
    """
    A trading bot that implements a Moving Average Crossover (MAC) strategy.

    Attributes:
        short_window (int): The window size for the short-term moving average.
        long_window (int): The window size for the long-term moving average.
        shares_amount (float): The amount of shares to buy or sell.

    Methods:
        execute_strategy(data): Executes the MAC strategy based on the given data.
    """

    def __init__(
        self,
        symbol,
        initial_cash,
        shares_amount,
        short_window,
        long_window,
        start_date,
        end_date,
    ):
        super().__init__(symbol, initial_cash, shares_amount, start_date, end_date)
        self.short_window = short_window
        self.long_window = long_window

    def execute_strategy(self, data):
        """
        Executes the moving average crossover strategy on the given data.

        Parameters:
        - data (pandas.DataFrame): The data used for the strategy.

        Returns:
        None
        """
        short_sma = self.calculate_sma(data, self.short_window)
        long_sma = self.calculate_sma(data, self.long_window)
        shares_amount = float(self.shares_amount)

        for i in range(self.long_window, len(data)):
            if short_sma[i] > long_sma[i]:
                self.buy(data["Close"][i], shares_amount)
            elif short_sma[i] < long_sma[i]:
                self.sell(data["Close"][i], shares_amount)
