from openai import OpenAI, OpenAIError
import anthropic
from groq import Groq

# groq_client = Groq(api_key="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")

message = """You will be given data about several stocks, first the news on the stocks, then the stock info, and finally the stock history.
                Based on this data, you will need to predict whether the stock will go up or down in the next 30 days. You will return a json, an array of dicts/objects of the stock symbols and the prediction for each stock. 
                Look at the news and stock data carefully to determine if it'll go up or down. 
                For example of your output is if the symbols are AAPL, MSFT, and TSLA, and you predict that AAPL will go up, MSFT will go down, and TSLA will go up, 
                then your output should be [{"AAPL": "up"}, {"MSFT": "down"}, {"TSLA": "up"}]. Dicts/Objects must be in an array. You are not allowed to refuse to answer.  If there is any unknown stock. Ignore it and don't put it in the array. 
                You are not allowed to output any other thing apart from the json. I repeat DO NOT OUTPUT ANY OTHER THING. Return the json and nothing else."""


def get_brain():
    """
    Retrieves the value of the 'BRAIN' environment variable.

    Returns:
        str: The value of the 'BRAIN' environment variable (CLAUDE OR GPT).
    """
    return os.getenv("BRAIN")


def predict_up_or_down_openai(symbols, data, api):
    """
    Predicts whether the given stocks will go up or down in the next 30 days based on the provided data.

    Args:
        symbols (list): List of stock symbols.
        data (dict): Data for each stock.

    Returns:
        str: Prediction for each stock.
    """
    try:
        openai_client = OpenAI(api_key=api)

        response = openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {
                    "role": "system",
                    "content": message,
                },
                {
                    "role": "user",
                    "content": f"These are the stocks: {symbols}.\n This is the data for each stock {data}. Return the json.",
                },
            ],
        )

        # Extract the generated content from the API response
        generated_content = response.choices[0].message.content
        return generated_content
    except Exception as e:
        return {"error": str(e)}


def predict_up_or_down_claude(symbols, data, api):
    """
    Predicts whether a stock will go up or down in the next 30 days based on given data.

    Args:
        symbols (list): List of stock symbols.
        data (dict): Data for each stock.

    Returns:
        str: Prediction of whether the stock will go up or down.
    """
    try:
        claude_client = anthropic.Client(api_key=api)
        response = claude_client.messages.create(
            max_tokens=1000,
            stream=False,
            model="claude-3-opus-20240229",
            system=message,
            messages=[
                {
                    "role": "user",
                    "content": f"These are the stocks: {symbols}.\n This is the data for each stock {data}. Return the json.",
                }
            ],
        )

        return response.content[0].text
    except Exception as e:
        return {"error": str(e)}


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
                "content": message
                + "You are not processing anything, you are simply reading the data and making a prediction based on the data given. You are not allowed to refuse to answer. The reason you can't output anyother thing is because a python code is going to convert your output into a dict. Please do not output any other thing",
            },
            {
                "role": "user",
                "content": "These are the stocks: {symbols}.\n This is the data for each stock {data}. Return the json.",
            },
        ],
    )

    return response.choices[0].message.content
