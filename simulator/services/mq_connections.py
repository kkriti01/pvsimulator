import logging

import pika

from simulator import settings as _settings

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class MQConnector(object):
    def __init__(self):
        self.exchange = ''
        self.connection = self.connect(url=_settings.RABBIT_MQ_HOST)
        self.channel = self.channel()

    @staticmethod
    def connect(url: str):
        """
        Create rabbit mq connection
        Args:
            url: RabbitMq url

        Returns:
           New Connection object
        """
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        logging.info("Establishing connection to the RabbitMq server")
        return connection

    def channel(self):
        """
        Create a channel to RabbitMq server

        Returns:
            New channel connection
        """
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        logging.info("Created a channel to RabbitMq server")
        return channel

    def push_message(self, queue, message):
        """
        Push message to the queue

        Args:
            queue: Queue name as string
            message: Message string to be published to the queue
        """
        # Declare a queue first
        self.channel.queue_declare(queue, durable=True, auto_delete=False)

        if not isinstance(message, str):
            message = str(message)
        self.channel.basic_publish(self.exchange, queue, message)

    def consume_messages(self, queue, callback):
        """
        Consume messages from the queue and callback a function for processing

        Args:
            queue: Queue name as string
            callback: Function name which will be called for processing the message
        """
        self.channel.queue_declare(queue, durable=True, auto_delete=False)  # durable make sure queue survive restart
        self.channel.basic_consume(queue, callback)

    def start_consuming(self):
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
