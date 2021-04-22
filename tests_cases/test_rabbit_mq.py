import json
import unittest

from config.constants import VHOST
from mq.connection import MQConnector


class TestRabbitMq(unittest.TestCase):
    def setUp(self) -> None:
        self.message = {"meter_reading": 10}
        self.connector = MQConnector(vhost=VHOST)

    def test_rabbitmq(self) -> None:
        # define your consumer
        def on_message(channel, method_frame, header_frame, body):
            body = json.loads(body.decode("utf-8").replace("'", '"'))
            assert self.message == body
            channel = self.connector.channel()
            channel.queue_delete(queue="test_queue")
            self.connector.close_connection()  # stops the consumer

        # define your publisher
        def publish_message(message):
            self.connector.push_message("test_queue", message)

        publish_message(self.message)
        self.connector.consume_queue("test_queue", on_message)