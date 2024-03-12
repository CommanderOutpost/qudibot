from trading_app.trading_bot import tradingbot as tb


class BollingerBandsStrategyTradingBot(tb.StockTradingBot):
    """
    A trading bot that implements the Bollinger Bands strategy.

    The Bollinger Bands strategy is a popular technical analysis tool that helps identify potential buying and selling opportunities in financial markets.

    Attributes:
        symbol (str): The symbol of the stock to trade.
        short_window (int): The window length for the short-term moving average.
        long_window (int): The window length for the long-term moving average.
        initial_cash (float): The initial amount of cash available for trading.
        shares_amount (float): The number of shares to buy/sell per trade.
        bollinger_window_length (int): The window length for calculating Bollinger Bands.
        bollinger_num_std_devs (int): The number of standard deviations to use for Bollinger Bands.

    Methods:
        execute_strategy(data): Executes the Bollinger Bands trading strategy on the specified historical stock data.
    """

    def __init__(
        self,
        symbol,
        initial_cash,
        shares_amount,
        bollinger_window_length,
        bollinger_num_std_devs,
    ):
        super().__init__(symbol, initial_cash, shares_amount, start_date, end_date)
        self.bollinger_window_length = bollinger_window_length
        self.bollinger_num_std_devs = bollinger_num_std_devs

    def execute_strategy(self, data):
        """
        Executes the Bollinger Bands trading strategy on the specified historical stock data.

        Args:
            data (pandas.DataFrame): The historical stock data.
        """
        window_length = int(self.bollinger_window_length)
        num_std_devs = int(self.bollinger_num_std_devs)
        shares_amount = float(self.shares_amount)

        # Calculate Bollinger Bands
        rolling_mean = data["Close"].rolling(window=window_length).mean()
        rolling_std = data["Close"].rolling(window=window_length).std()
        upper_band = rolling_mean + (num_std_devs * rolling_std)
        lower_band = rolling_mean - (num_std_devs * rolling_std)

        # Execute trades
        for i in range(window_length, len(data)):
            if data["Close"][i] <= lower_band[i]:
                # Buy signal: stock price touches lower band
                self.buy(data["Close"][i], shares_amount)
            elif data["Close"][i] >= upper_band[i]:
                # Sell signal: stock price touches upper band
                self.sell(data["Close"][i], shares_amount)
