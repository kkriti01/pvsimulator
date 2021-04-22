# Produce messages to the broker with random but continuous values from 0 to 9000 Watts.
import logging
import random
import time
from datetime import datetime

from config.constants import MIN_POWER_CONSUMPTION, MAX_POWER_CONSUMPTION
from mq.produce_messages import MQProducer


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_power_consumption() -> int:
    """
    Return random meter power generated in range of [0, 9000] watt
    """
    return random.randrange(MIN_POWER_CONSUMPTION, MAX_POWER_CONSUMPTION)


def publish_message(meter_reading: int) -> None:
    """
    Publish generated meter power reading to pv_simulator service
    """
    current_timestamp = datetime.today()
    data = {"time_of_reading": current_timestamp.strftime('%Y-%m-%dT%H:%M:%S'), "meter_power_value": meter_reading}

    logging.info("Data getting published to the PV broker is: {}".format(data))
    mq = MQProducer(data)
    mq.produce()


def run():
    """
    Steps:
    Step 1: Generate random meter power readings
    Step 2: Publish generated meter power readings to pv_simulator
    Step 3: Sleep it for 60 second and then run publish messages again
    """

    while True:

        # Step 1:
        logging.info("Started meter reading at {}".format(datetime.today()))
        meter_reading = get_power_consumption()
        logging.info("Meter reading on time: {} is {}".format(datetime.today(), meter_reading))

        # Step 2:
        publish_message(meter_reading)
        logging.info("Meter reading is published to PV broker")

        # Step 3:
        time.sleep(60)

run()