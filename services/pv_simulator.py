# Generate a simulated PV power value and the last step is to add this value to the meter value and output the result.
import json
import os
from datetime import datetime

import pandas as pd
import random


def get_power_meter_reading(data: bytes) -> dict:
    """
    Reads power consumption meter reading published from meter reading
    """
    return json.loads(data.decode("utf-8").replace("'", '"'))


def simulate_power_value(data: dict) -> int:
    """
    Steps
    1. Get power meter reading
    2.
    """
    # I  am assuming here that pv simulation will take power meter as input and will generate some output which
    # I am taking some random number
    return random.randint(0, 10)


def write_reading_to_file(data: dict):
    df = pd.DataFrame(data, index=["time_of_reading", "meter_power_value", "pv_power_value", "simulated_power"])
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "power_reading_file")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    file_name = os.path.join(output_dir, "Meter_reading_on_{}_.csv".format(datetime.now().strftime('%Y-%m-%d')))
    if not os.path.isfile(file_name):
        df.to_csv(file_name, mode='a', index=False)
    else:
        df.to_csv(file_name, mode='a', index=False, header=False)


def run_simulator(data: bytes) -> None:
    """
    # Steps:
    Step 1: Get power meter reading
    Step 2: Simulate power value
    Step 3: Add simulated value obtained in step 2 with power meter reading obtained in step 1
    Step 4: Add data obtained in step 3 to a file.
    """

    # Step 1:
    meter_reading = get_power_meter_reading(data)

    # Step 2:
    power_value = simulate_power_value(meter_reading)
    meter_reading["pv_power_value"] = power_value

    # Step 3:
    power_value += meter_reading["meter_power_value"]
    meter_reading["simulated_power"] = power_value

    # Step 4:
    write_reading_to_file(meter_reading)
