import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError

from public_api.settings.env_configs_models import Settings
from public_api.settings.logging_c_formatter import CustomFormatter, CustomFormatterNoColor


root_logger = logging.getLogger()

tortoise_loggers = ['tortoise', 'tortoise.models', 'tortoise.orm', 'tortoise.transactions', 'tortoise.fields',
                    'tortoise.fields.relational']
uvicorn_logger = ['uvicorn', 'uvicorn.error', 'uvicorn.access']

all_removed_loggers = tortoise_loggers + uvicorn_logger
env_paths = ['..', '']
debug_mode_flags = [1, True, 'true', 'True', '1', None]

for _p in env_paths:
    base_path = os.path.join(_p, '.env')
    if os.path.exists(base_path):
        with open(os.path.join(base_path), 'r') as file:
            load_dotenv(stream=file)
        break

for _h in root_logger.handlers:
    root_logger.removeHandler(_h)

debug = os.environ.get('DEBUG_MODE') in debug_mode_flags
if debug:
    root_logger.setLevel(logging.INFO)
    root_logger.info('Starting in DEBUG mode')
    for _t in all_removed_loggers:
        logging.getLogger(_t).setLevel(logging.INFO)
else:
    root_logger.setLevel(logging.INFO)
    root_logger.info('Starting in PRODUCTION mode')
    for _t in all_removed_loggers:
        logging.getLogger(_t).setLevel(logging.ERROR)

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(CustomFormatter())
root_logger.addHandler(consoleHandler)


# Path to logs folder
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'app.log')

file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=14)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatterNoColor())

root_logger.addHandler(file_handler)

for _t in all_removed_loggers:
    l = logging.getLogger(_t)
    l.addHandler(consoleHandler)
    l.addHandler(file_handler)

_logger = logging.getLogger(__name__)

try:
    settings = Settings(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg='Env parameters validation error')
    sys.exit(-1)
