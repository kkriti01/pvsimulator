import pathlib

MIN_HOME_POWER_CONSUMPTION = 0
MAX_HOME_POWER_CONSUMPTION = 9000

PV_SIMULATOR_MIN_WEIGHT = 0.2
PV_SIMULATOR_MAX_WEIGHT = 0.5

# MQ Config
MQ_HOST = "amqp://guest:guest@localhost:5672/PVSimulator"
POWER_METER_QUEUE = 'power_meter_reading'
VHOST = 'PVSimulator'

LOG_DIR_PATH = pathlib.Path(__file__).joinpath('logs')
