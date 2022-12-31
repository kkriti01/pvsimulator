import logging
import random
import time
from datetime import datetime

from simulator import settings as _settings
from simulator.services.mq_connections import MQConnector

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_meter_reading() -> int:
    """
    Simulate home meter power reading.

    Returns:
        random power value between (0, 9000 watts)
    """
    return random.randint(_settings.MIN_POWER_READING, _settings.MAX_POWER_READING)


def publish_message(meter_reading: int) -> None:
    """
    Publish power consumption to the broker

    Note: Publishing the reading in watt for future implementations

    Args:
        meter_reading: Meter reading value for every time interval from meter broker
    """
    current_timestamp = datetime.now()
    data = {"time_of_reading": current_timestamp.strftime('%Y-%m-%dT%H:%M:%S'), "meter_power_value": meter_reading}

    connector = MQConnector()
    connector.push_message(_settings.POWER_METER_QUEUE, data)
    logging.info("Published message: {} to queue".format(data))


def run():
    """
    Run this script to read the meter reading and publishing it to the queue
    """

    while True:
        logging.info("********* Starting to read meter reading *****************")
        meter_reading = get_meter_reading()
        publish_message(meter_reading)
        time.sleep(1)


if __name__ == '__main__':
    run()
