import datetime
import json
import time
import random
import os
import logging
from trading_app.db import get_db

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_30_days_ago():
    return (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")


def save_to_file(data, filename):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.error(f"Error saving data to file {filename}: {e}")


def typing_simulator(text):
    # Randomize the typing speed
    for letter in text:
        try:
            sleep_time = random.uniform(0.00009, 0.009)
            print(letter, end="", flush=True)
            time.sleep(sleep_time)
        except Exception as e:
            logging.error(f"Error during typing simulation: {e}")
            break
    print()


def pause():
    try:
        gap_time = random.uniform(0.8, 1.2)
        time.sleep(gap_time)
    except Exception as e:
        logging.error(f"Error during pause: {e}")


def convert_timestamp_keys_to_string(input_dict):
    """
    Convert timestamp keys in a dictionary to string representation.

    Args:
        input_dict (dict): The dictionary containing timestamp keys.

    Returns:
        dict: The dictionary with timestamp keys converted to string representation.
    """
    converted_dict = {}

    for key, value in input_dict.items():
        for keys, values in value.items():
            for k, v in values.items():
                if isinstance(k, datetime.datetime):
                    try:
                        # Convert timestamp to string representation
                        k = k.strftime("%Y-%m-%d %H:%M:%S")
                        converted_dict[k] = v
                    except Exception as e:
                        logging.error(f"Error converting timestamp key to string: {e}")
            value[keys] = converted_dict
            converted_dict = {}

    return input_dict


def add_trade_to_db(trade):
    db = get_db()
    # cursor = db.cursor()

    # Insert the new trade
    db.execute(
        """
        INSERT INTO trade (stock, start_date, end_date, strategy, cash_balance, user_id, time_started, 
        time_ended, profit, status, type, history, stock_balance, portfolio_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            trade["stock"],
            trade["start_date"],
            trade["end_date"],
            trade["strategy"],
            trade["cash_balance"],
            trade["user_id"],
            trade["time_started"],
            trade["time_ended"],
            trade["profit"],
            trade["status"],
            trade["type"],
            trade["history"],
            trade["stock_balance"],
            trade["portfolio_value"],
        ),
    )
    trade_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

    db.commit()

    return trade_id


def update_trade_columns(trade_id, column_values):
    db = get_db()

    # Update the specified columns for the trade with the given trade_id
    for column_name, new_value in column_values.items():
        db.execute(
            f"UPDATE trade SET {column_name}=? WHERE id=?", (new_value, trade_id)
        )

    db.commit()


def get_from_table(table_name, filters):
    db = get_db()

    # Construct the SQL query
    query = f"SELECT * FROM {table_name}"
    if filters:
        conditions = []
        values = []
        for column, value in filters.items():
            conditions.append(f"{column}=?")
            values.append(value)
        query += " WHERE " + " AND ".join(conditions)

    # Execute the query
    rows = db.execute(query, tuple(values)).fetchall()

    # Convert rows to a list of dictionaries
    result = []
    for row in rows:
        row_dict = dict(row)
        result.append(row_dict)

    return result


# Function to clear all trades from the database
def clear_trades(user_id):
    db = get_db()

    # Clear trades from the database for the specified user_id
    db.execute("DELETE FROM trade WHERE user_id=?", (user_id,))

    db.commit()
