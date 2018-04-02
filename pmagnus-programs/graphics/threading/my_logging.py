import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info('Start reading database')
records = {'john' : 55, 'tom' : 66}

logger.debug('Records: %s', records)
logger.info('Updating records ...')

logger.info('Finish updating records')