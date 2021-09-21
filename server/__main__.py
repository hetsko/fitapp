from app import get_fitapp, Data
import logging
import random
logging.basicConfig(level=logging.INFO, format='%(message)s')

# fit = get_fitapp()
fit = get_fitapp(open_browser=False)

# Setup testing data
fit.labels = ['1', '2', '3']
fit.callback_data(lambda i: Data(
    x=list(range(int(i) + 4)),
    y=[a + -1 + 2*random.random() for a in range(int(i) + 4)]
))


@fit.set_fitfunc
def func(x, a, b):
    return a*x + b


try:
    # fit._wait_forever()
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info('Detected CTRL-C. Exiting...')
