from . import get_fitapp, Data

import random
import logging
import numpy


def create_test(log=True):
    if log:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    fit = get_fitapp(open_browser=False, http_log=True)

    # Setup testing data
    fit.labels = numpy.array([(21000+i, i) for i in range(1, 15)])

    @fit.callback_data
    def get_data(ii):
        return Data(
            x=list(range(20)),
            y=[ii[1]*x + -1 + 2*random.random() for x in range(20)],
            yerr=[2 for _ in range(20)],
        )

    @fit.set_fitfunc
    def func(x, a, b):
        return a*x + b

    @fit.callback_guess
    def get_guess(ii):
        return [1, 0]

    return fit
