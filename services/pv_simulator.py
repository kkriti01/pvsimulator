import json
import logging
import os
import time
import random
from datetime import datetime

import pandas as pd

from services.broker import MQConnector
from settings import POWER_METER_QUEUE, LOG_DIR_PATH, PV_SIMULATOR_MIN_WEIGHT, PV_SIMULATOR_MAX_WEIGHT,\
    LOG_FILE_NAME_TEMPLATE

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_current_time_weight() -> float:
    """
    Poor man time wight value

    get a weight value from current time for PV power simulation

    this is so simulate that power of a PV cell increase from 4 AM to 12 noon and then
    start decreasing .
    """
    now = datetime.now()
    hour = float(now.strftime('%-I'))
    minute = float(now.strftime('%-M'))
    time_weight = hour + (minute / 60)
    if now.strftime('%p') == "PM":
        time_weight = 12 - time_weight
    return time_weight


def get_simulated_power_value():
    """
    Poor man Simulation of PV power, weighted by current time.
    """
    current_time_weight = get_current_time_weight()
    return current_time_weight * random.uniform(PV_SIMULATOR_MIN_WEIGHT, PV_SIMULATOR_MAX_WEIGHT)


def write_reading_to_file(data: dict):
    LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)  # create dir if does not exist

    df = pd.DataFrame(data, index=["timestamp", "meter", "pv_power", "sum"])
    file_path = LOG_DIR_PATH.joinpath(LOG_FILE_NAME_TEMPLATE.format(datetime.now().strftime('%Y-%m-%d')))
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', index=False, header=False)


def read_power_data(data: dict) -> None:
    """
    Poor man PV Simulator

    Simulate PV power and write to log file.
    """

    # read meter
    meter_power = data['meter_power_value']  # in Watt

    # Get PV power
    pv_power = get_simulated_power_value()  # in Kilo Watt

    # sum of the power
    total_power = pv_power + (meter_power / 1000)  # Kilo Watt

    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'meter': meter_power,  # Watt
        'pv_power': pv_power,  # kilo Watt
        'sum': total_power,  # kilo Watt
    }
    write_reading_to_file(data)


def simulator(channel, method_frame, header_frame, body):
    """
    callback to rabbitmq connection

    """
    body = json.loads(body.decode("utf-8").replace("'", '"'))
    read_power_data(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':

    while True:
        logging.info("*** PV Simulator started ***")
        connector = MQConnector()
        connector.consume_queue(POWER_METER_QUEUE, simulator)
        connector.start_consuming()
        time.sleep(1)
