import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from app import get_fitapp

fit = get_fitapp()
try:
    fit._wait_forever()
except KeyboardInterrupt:
    logging.info('Detected CTRL-C. Exiting...')
