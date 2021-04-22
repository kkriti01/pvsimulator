import logging

from config.constants import POWER_METER_READING_QUEUE, VHOST
from mq.connection import MQConnector


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class MQProducer(object):
    def __init__(self, data) -> None:
        self.data = data

    def produce(self) -> None:
        connector = MQConnector(vhost=VHOST)
        connector.push_message(POWER_METER_READING_QUEUE, self.data)
        logging.info("Published message: {} to queue".format(self.data))


if __name__ == '__main__':
    mq = MQProducer({"reading": 100})
    mq.produce()