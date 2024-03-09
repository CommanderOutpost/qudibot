import json
import feedparser
import logging

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
}

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_news_for_stock(stock_symbol):
    """
    Retrieves news headlines for a given stock symbol.

    Args:
        stock_symbol (str): The symbol of the stock.

    Returns:
        list: A list of dictionaries containing news headlines and summaries.
    """
    rssfeedurl = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US"
        % stock_symbol
    )
    try:
        NewsFeed = feedparser.parse(rssfeedurl)
        all_news = []
        for news in NewsFeed.entries:
            all_news.append({"title": news.title, "news": news.summary})
        return all_news
    except Exception as e:
        logging.error(f"Error retrieving news for {stock_symbol}: {e}")
        return []


def get_news_for_all_stocks(stock_symbols):
    """
    Retrieves news data for multiple stock symbols.

    Args:
        stock_symbols (list): List of stock symbols.

    Returns:
        dict: A dictionary containing news data for each stock symbol.
    """
    all_news = {}
    for stock_symbol in stock_symbols:
        try:
            all_news[stock_symbol] = get_news_for_stock(stock_symbol)
        except Exception as e:
            logging.error(f"Error retrieving news for {stock_symbol}: {e}")
            all_news[stock_symbol] = []
    return all_news
