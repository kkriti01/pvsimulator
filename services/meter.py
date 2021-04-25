import logging
import random
import time
from datetime import datetime

from services.broker import MQConnector
from settings import MIN_HOME_POWER_CONSUMPTION, MAX_HOME_POWER_CONSUMPTION, POWER_METER_QUEUE

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_power_consumption() -> int:
    """
    Simulate home power consumption in Watts
    """
    return random.randrange(MIN_HOME_POWER_CONSUMPTION, MAX_HOME_POWER_CONSUMPTION)


def publish_message(meter_reading: int) -> None:
    """
    Publish power consumption to the broker
    """
    current_timestamp = datetime.now()
    data = {"time_of_reading": current_timestamp.strftime('%Y-%m-%dT%H:%M:%S'), "meter_power_value": meter_reading}

    connector = MQConnector()
    connector.push_message(POWER_METER_QUEUE, data)
    logging.info("Published message: {} to queue".format(data))


def run():
    """
    publish meter reading data to thr queue
    """
    while True:
        logging.info('** Started meter reading ** ')
        meter_reading = get_power_consumption()

        publish_message(meter_reading)
        time.sleep(1)


if __name__ == '__main__':
    run()

