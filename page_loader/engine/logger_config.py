import logging
import sys

LOG_FORMAT = '%(asctime)s %(message)s'
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

# create logger
logger = logging.getLogger('logger')
logger_error = logging.getLogger('logger_error')


logger.setLevel(logging.INFO)
logger_error.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
ch_error = logging.StreamHandler()

# create formatter
formatter = logging.Formatter(datefmt=DATE_FORMAT, fmt=LOG_FORMAT)

# add formatter to ch and ch_error
ch.setFormatter(formatter)
ch_error.setFormatter(formatter)

# add ch to logger and logger_error
logger.addHandler(ch)
logger_error.addHandler(ch_error)
