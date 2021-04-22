import logging

from config.constants import POWER_METER_READING_QUEUE, VHOST
from mq.connection import MQConnector
from services.pv_simulator import run_simulator

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class MQConsumer(object):
    def __init__(self, queue) -> None:
        self.queue = queue

    @staticmethod
    def call_back(channel, method_frame, header_frame, body):
        logging.info("Message received is {}".format(body))
        run_simulator(body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def consume(self) -> None:
        connector = MQConnector(vhost=VHOST)
        logging.info("Consumer started")
        connector.consume_queue(POWER_METER_READING_QUEUE, self.call_back)
        connector.start_consuming()


if __name__ == '__main__':
    mq = MQConsumer(POWER_METER_READING_QUEUE)
    mq.consume()
