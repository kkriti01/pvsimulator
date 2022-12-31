import os
import pathlib

MIN_POWER_READING = int(os.environ.get('MIN_POWER_READING', '0'))
MAX_POWER_READING = int(os.environ.get('MAX_POWER_READING', '9000'))
MAX_POWER_ROUND = 4

POWER_METER_QUEUE = os.environ.get('POWER_METER_QUEUE', 'power_meter_reading')
SIMULATOR_MIN_WEIGHT = float(os.environ.get('SIMULATOR_MIN_WEIGHT', '0.2'))
SIMULATOR_MAX_WEIGHT = float(os.environ.get('SIMULATOR_MAX_WEIGHT', '0.5'))

RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST', 'amqp://guest:guest@localhost:5672')

LOG_DIR_PATH = pathlib.Path(__file__).parent.parent.joinpath('logs')  # if you change this, also change in docker-compose
print(LOG_DIR_PATH)
LOG_FILE_NAME_TEMPLATE = 'pv_power_simulation_{}_.csv'
