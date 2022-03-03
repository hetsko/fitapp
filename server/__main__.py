from ._test import create_test
import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

fit = create_test(local=sys.argv[1] != 'public')
try:
    # fit._wait_forever()
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info('Detected CTRL-C. Exiting...')
