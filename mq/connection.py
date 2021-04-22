import logging

import pika

from config.constants import MQ_HOST

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

MQ_URL_MAP = {
    'PVSimulator': MQ_HOST,
}


class MQConnector:
    def __init__(self, vhost='PVSimulator'):
        self.exchange = ''
        self.connection = self.connect(url=MQ_URL_MAP[vhost])
        self.channel = self.channel()

    def connect(self, url):
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        logging.info("Established connection to RabbitMQ server")
        return connection

    def channel(self):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        logging.info("Created a channel to RabbitMQ server")
        return channel

    def push_message(self, queue, message):
        self.channel.queue_declare(queue, durable=True, auto_delete=False)
        if not isinstance(message, str):
            message = str(message)
        self.channel.basic_publish(self.exchange, queue, message)

    def consume_queue(self, queue, callback):
        self.channel.queue_declare(queue, durable=True, auto_delete=False)
        self.channel.basic_consume(queue, callback)

    def start_consuming(self):
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
