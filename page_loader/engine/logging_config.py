import logging

LOG_FORMAT = '%(message)s'

log = logging.getLogger(__name__)

logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.INFO)
logger_format = logging.Formatter(LOG_FORMAT)
logger_handler.setFormatter(logger_format)
log.addHandler(logger_handler)
