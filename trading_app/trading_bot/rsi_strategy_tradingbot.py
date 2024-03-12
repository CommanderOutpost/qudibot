from trading_app.trading_bot import tradingbot as tb


class RSIStrategyTradingBot(tb.StockTradingBot):
    """
    A trading bot that implements a strategy based on the Relative Strength Index (RSI).

    Args:
        symbol (str): The symbol of the stock to trade.
        short_window (int): The window length for the short moving average.
        long_window (int): The window length for the long moving average.
        initial_cash (float): The initial amount of cash available for trading.
        shares_amount (float): The number of shares to buy/sell for each trade.
        rsi_window_length (int): The window length for calculating the RSI.
        rsi_overbought_threshold (float): The threshold above which the RSI is considered overbought.
        rsi_oversold_threshold (float): The threshold below which the RSI is considered oversold.

    Methods:
        execute_strategy(data): Executes the RSI trading strategy on the specified historical stock data.
    """

    def __init__(
        self,
        symbol,
        initial_cash,
        shares_amount,
        rsi_window_length,
        rsi_overbought_threshold,
        rsi_oversold_threshold,
        start_date,
        end_date,
    ):
        super().__init__(
            symbol,
            initial_cash,
            shares_amount,
        )
        self.rsi_window_length = rsi_window_length
        self.rsi_overbought_threshold = rsi_overbought_threshold
        self.rsi_oversold_threshold = rsi_oversold_threshold

    def execute_strategy(self, data):
        """
        Executes the RSI strategy trading algorithm.

        Parameters:
        - data (pandas.DataFrame): The input data containing the stock prices.

        Returns:
        None
        """
        window_length = int(self.rsi_window_length)
        overbought_threshold = float(self.rsi_overbought_threshold)
        oversold_threshold = float(self.rsi_oversold_threshold)
        shares_amount = float(self.shares_amount)

        # Calculate RSI
        delta = data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window_length).mean()
        avg_loss = loss.rolling(window=window_length).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        for i in range(window_length, len(data)):
            if rsi[i] > overbought_threshold:
                # Sell signal: RSI is above the overbought threshold
                self.sell(data["Close"][i], shares_amount)
            elif rsi[i] < oversold_threshold:
                # Buy signal: RSI is below the oversold threshold
                self.buy(data["Close"][i], shares_amount)
