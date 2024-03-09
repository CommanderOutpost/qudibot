from flaskr import utils
from flaskr.stock_data import get_news_data, get_stock_data
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def gather_data(symbols):
    """
    Gather data for the given symbols.

    Args:
        symbols (list): List of symbols for which data needs to be gathered.

    Returns:
        dict: A dictionary containing the gathered data, including news data, stock info, and stock history.
    """
    start_date = utils.get_30_days_ago()
    end_date = utils.get_today()

    try:
        news_data = get_news_data.get_news_for_all_stocks(symbols)
    except Exception as e:
        logging.error(f"Error retrieving news data: {e}")
        news_data = {}

    try:
        stock_info = get_stock_data.get_stock_info(symbols)
    except Exception as e:
        logging.error(f"Error retrieving stock info: {e}")
        stock_info = {}

    try:
        stock_history = get_stock_data.get_stock_data(symbols, start_date, end_date)
        stock_history = utils.convert_timestamp_keys_to_string(stock_history)
    except Exception as e:
        logging.error(f"Error retrieving stock history: {e}")
        stock_history = {}

    # Put all in one dictionary
    all_data = {
        "news": news_data,
        "stock_info": stock_info,
        "stock_data": stock_history,
    }

    return all_data
