import logging

import pika

from settings import RABBIT_MQ_HOST

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class MQConnector:
    def __init__(self):
        self.exchange = ''
        self.connection = self.connect(url=RABBIT_MQ_HOST)
        self.channel = self.channel()

    @staticmethod
    def connect(url):
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
