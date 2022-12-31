import csv
import datetime
import json
import os
import random
import time

from simulator import settings as _settings
from simulator.services.mq_connections import MQConnector


def get_current_time_weight() -> float:
    """
    Get current time weight value.
    This is to simulate that power of a PV cell increases from 4AM to 12 Noon and then start decreasing.

    Returns: Time weight at different interval to simulate PV value
    """
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    time_weight = hour + (minute/60)

    if now.strftime("%p") == "PM":
        time_weight = time_weight - 12

    return time_weight


def get_simulated_power_value() -> float:
    """
    Get simulated time-weighted power value for each time period

    Returns:
        simulated time-weighted power value
    """
    current_time_weight = get_current_time_weight()

    return round((current_time_weight * random.uniform(_settings.SIMULATOR_MIN_WEIGHT, _settings.SIMULATOR_MAX_WEIGHT)),
                 _settings.MAX_POWER_ROUND)


def write_power_to_file(data: dict) -> None:
    """
    Write power value recorded at each time to file

    Args:
        data: Power data reading and simulated power at different time intervals
    """

    header = ["timestamp", "meter_power", "pv_power", "sum"]
    _settings.LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)  # create dir if does not exist

    file_path = _settings.LOG_DIR_PATH.joinpath(_settings.LOG_FILE_NAME_TEMPLATE.format(datetime.datetime.now().
                                                                                        strftime('%Y-%m-%d')))
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
        f.close()


def simulate_power(data: dict) -> dict:
    """
    1. Read meter power value from broker
    2. Generate a simulated PV power value
    3. Add meter value to simulated PV power value
    4. Write the results to file

    Args:
        data: Meter reading data

    Returns:
        data: Updated dictionary with pv simulated power sum
    """

    # Meter power reading
    meter_power = data["meter_power_value"]
    meter_power = round(meter_power / 1000, _settings.MAX_POWER_ROUND)  # kilo watt to make it uniform across system

    # Get PV power
    pv_power = get_simulated_power_value()  # In kilo watt

    # Sum of the power
    total_power = round((pv_power + meter_power), _settings.MAX_POWER_ROUND)

    data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "meter_power": meter_power,
        "pv_power": pv_power,
        "sum": total_power
    }

    return data


def process_messages(channel , method_frame, header_frame, body):
    """
    Consume message from mq and process it
    1. Simulate PV power and meter power
    2. Write simulated power to file

    Args:
        body: Message consumed from the queue
    """
    body = json.loads(body.decode("utf-8").replace("'", '"'))
    data = simulate_power(body)

    # Write the PV results to file
    write_power_to_file(data)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    while True:
        connector = MQConnector()
        connector.consume_messages(_settings.POWER_METER_QUEUE, process_messages)
        connector.start_consuming()
        time.sleep(1)
