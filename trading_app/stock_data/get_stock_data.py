import yfinance as yf
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_stock_data(symbols, start_date, end_date):
    """
    Retrieves stock data for multiple stock symbols within a given date range.

    Args:
        symbols (list): List of stock symbols.
        start_date (str): Start date in the format "YYYY-MM-DD".
        end_date (str): End date in the format "YYYY-MM-DD".

    Returns:
        dict: A dictionary containing stock data for each symbol.
    """
    stock_data = {}
    for symbol in symbols:
        try:
            stock_data[symbol] = yf.download(
                symbol, start=start_date, end=end_date
            ).to_dict()
        except Exception as e:
            logging.error(f"Error retrieving stock data for {symbol}: {e}")
            stock_data[symbol] = {}
    return stock_data


def get_stock_info(symbols):
    """
    Retrieves stock information for multiple stock symbols.

    Args:
        symbols (list): List of stock symbols.

    Returns:
        dict: A dictionary containing stock information for each symbol.
    """
    stock_info = {}
    for symbol in symbols:
        try:
            stock_info[symbol] = yf.Ticker(symbol).info
        except Exception as e:
            logging.error(f"Error retrieving stock information for {symbol}: {e}")
            stock_info[symbol] = {}
    return stock_info
