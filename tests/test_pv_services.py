import json
import unittest

from simulator.services.meter import get_meter_reading
from simulator.services.pv_simulator import simulate_power
from simulator import settings as _settings
from simulator.services.mq_connections import MQConnector


class TestPVServices(unittest.TestCase):
    def setUp(self) -> None:
        self.message = {"meter_power_value": 10}
        self.connector = MQConnector()

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
        self.connector.consume_messages("test_queue", on_message)

    def test_meter_reading(self):
        meter_reading = get_meter_reading()

        assert _settings.MIN_POWER_READING <= meter_reading <= _settings.MAX_POWER_READING

    def test_simulator(self):
        expected_meter_power = round(self.message["meter_power_value"]/1000, 4)
        simulated_power = simulate_power(self.message)

        assert simulated_power["meter_power"] == expected_meter_power
        assert simulated_power["sum"] == round((expected_meter_power + simulated_power["pv_power"]), 4)

