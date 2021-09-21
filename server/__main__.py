from app import get_fitapp, Data
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# fit = get_fitapp()
fit = get_fitapp(open_browser=False)

# Setup testing data
fit.labels = ['1', '2', '3']
fit.callback_data(lambda i: Data(
    x=list(range(int(i) + 4)),
    y=(int(i) + 4)*[1]
))

try:
    # fit._wait_forever()
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info('Detected CTRL-C. Exiting...')
