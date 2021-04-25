import pathlib
import os

MIN_HOME_POWER_CONSUMPTION = int(os.environ.get('MIN_HOME_POWER_CONSUMPTION', '0'))
MAX_HOME_POWER_CONSUMPTION = int(os.environ.get('MAX_HOME_POWER_CONSUMPTION', '9000'))

PV_SIMULATOR_MIN_WEIGHT = float(os.environ.get('PV_SIMULATOR_MIN_WEIGHT', '0.2'))
PV_SIMULATOR_MAX_WEIGHT = float(os.environ.get('PV_SIMULATOR_MAX_WEIGHT', '0.5'))

RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST', 'amqp://guest:guest@rabbitmq:5672')
POWER_METER_QUEUE = os.environ.get('POWER_METER_QUEUE', 'power_meter_reading')

LOG_DIR_PATH = pathlib.Path(__file__).parent.joinpath('logs')  # if you change this, also change in docker-compose

LOG_FILE_NAME_TEMPLATE = 'pv_simulation_{}_.csv'
