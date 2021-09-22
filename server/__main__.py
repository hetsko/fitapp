from app import get_fitapp, Data
import logging
import random
logging.basicConfig(level=logging.INFO, format='%(message)s')

# fit = get_fitapp()
fit = get_fitapp(open_browser=False, http_log=True)

# Setup testing data
fit.labels = [f'{21000+i}/{i}' for i in range(1, 15)]


@fit.callback_data
def get_data(i):
    return Data(
        x=list(range(20)),
        y=[int(i.split('/')[-1])*x + -1 + 2*random.random() for x in range(20)]
    )


@fit.set_fitfunc
def func(x, a, b):
    return a*x + b


@fit.callback_guess
def get_guess(i):
    return [1, 0]


try:
    # fit._wait_forever()
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info('Detected CTRL-C. Exiting...')
