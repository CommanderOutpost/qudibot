import datetime
import json
import time
import random
import os
import logging

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
