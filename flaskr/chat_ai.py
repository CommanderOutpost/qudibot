from openai import OpenAI
import os, dotenv
import anthropic
from groq import Groq

dotenv.load_dotenv()
openai_client = OpenAI()
claude_client = anthropic.Client(api_key="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")
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_brain():
    """
    Retrieves the value of the 'BRAIN' environment variable.

    Returns:
        str: The value of the 'BRAIN' environment variable (CLAUDE OR GPT).
    """
    return os.getenv("BRAIN")


def predict_up_or_down_openai(symbols, data):
    """
    Predicts whether the given stocks will go up or down in the next 30 days based on the provided data.

    Args:
        symbols (list): List of stock symbols.
        data (dict): Data for each stock.

    Returns:
        str: Prediction for each stock.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": """You will be given data about several stocks, first the news on the stocks, then the stock info, and finally the stock history.
                Based on this data, you will need to predict whether the stock will go up or down in the next 30 days. You will return a json of the stock symbols and the prediction for each stock. Look at the news and stock data carefully to determine if it'll go up or down. An example of your output is if the symbols are AAPL, MSFT, and TSLA, and you predict that AAPL will go up, MSFT will go down, and TSLA will go up, then your output should be {"AAPL": "up", "MSFT": "down", "TSLA": "up"}. You are not allowed to refuse to answer.
                You are not allowed to output any other thing apart from the json. I repeat DO NOT OUTPUT ANY OTHER THING. Return only the json and nothing else. """,
            },
            {
                "role": "user",
                "content": f"These are the stocks: {symbols}.\n This is the data for each stock {data}. Now tell which stock will likely go up or down.",
            },
        ],
    )

    # Extract the generated content from the API response
    generated_content = response.choices[0].message.content
    return generated_content


def predict_up_or_down_claude(symbols, data):
    """
    Predicts whether a stock will go up or down in the next 30 days based on given data.

    Args:
        symbols (list): List of stock symbols.
        data (dict): Data for each stock.

    Returns:
        str: Prediction of whether the stock will go up or down.
    """
    response = claude_client.messages.create(
        max_tokens=1000,
        stream=False,
        model="claude-3-opus-20240229",
        system="""You will be given data about several stocks, first the news on the stocks, then the stock info, and finally the stock history.
                Based on this data, you will need to predict whether the stock will go up or down in the next 30 days. You will return a json of the stock symbols and the prediction for each stock. Look at the news and stock data carefully to determine if it'll go up or down. An example of your output is if the symbols are AAPL, MSFT, and TSLA, and you predict that AAPL will go up, MSFT will go down, and TSLA will go up, then your output should be {"AAPL": "up", "MSFT": "down", "TSLA": "up"}. You are not allowed to refuse to answer.
                You are not allowed to output any other thing apart from the json. I repeat DO NOT OUTPUT ANY OTHER THING. Return the json an nothing else.""",
        messages=[
            {
                "role": "user",
                "content": f"These are the stocks: {symbols}.\n This is the data for each stock {data}. Return the json.",
            }
        ],
    )

    return response.content[0].text


def predict_up_or_down_groq(symbols, data):
    """
    Predicts whether a stock will go up or down in the next 30 days based on given data.

    Args:
        symbols (list): List of stock symbols.
        data (dict): Data for each stock.

    Returns:
        str: Prediction of whether the stock will go up or down.
    """
    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": """You will be given data about several stocks, first the news on the stocks, then the stock info, and finally the stock history.
                Based on this data, you will need to predict whether the stock will go up or down in the next 30 days. Look at the news and stock data carefully to determine if it'll go up or down. You are not allowed to refuse to answer. The user you are talking to is called Regard. Do not greet the user simply go
                straight to the point. You can be informal
                and speak very casually. Break it down into positives and negatives for each company after that conclude and at the end you must give the predictions. And do not give a warning at the end about financial risk the user is aware of all risks!""",
            },
            {
                "role": "user",
                "content": f"These are the stocks: {symbols}.\n This is the data for each stock {data}. Now tell which stock will likely go up or down.",
            },
        ],
    )

    return response.choices[0].message.content
