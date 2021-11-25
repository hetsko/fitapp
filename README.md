# FitAPP

Interactively plot 1D data and fit it with custom models from the comfort
of your browser window. The main goal is to provide a simple and efficient
GUI for the well known function `scipy.optimize.curve_fit()`. Use cases:

- An alternative to interactive `matplotlib` plots in `jupyter notebook`
  (with limited functionality).
- I need to fit these 50 heat flux profiles by hand until lunch. It would
  really help if I could...
    - quickly adjust the initial parameters when needed
    - discard obvious outliers from the fitted dataset
    - inspect the resulting curve

The frontend is written using the [Svelte](https://svelte.dev) framework and
it communicates with python (to load data, calculate the fit, etc.) via a local
[Flask](https://flask.palletsprojects.com/) server.

## Install

Clone the repo to your machine:
```bash
git clone -b build https://github.com/hetsko/fitapp.git
```
The option `-b build` selects the build branch, which includes (hopefully)
the latest version of the javascript build, which is required to run the app.

> Alternatively, see section **Development** for instructions on how
> to build the frontend yourself.

## Usage

Import as any other python package and create a new instance of the app:
```python
from fitapp.server import get_fitapp, Data

# 1. Create the app, register labels (arbitrary names for your data sets).
fit = get_fitapp(port=8282)
fit.labels = ['data1', 'data2']

# 2. A new tab with the app should be launched automatically in your default
#    web browser (http://127.0.0.1:8282)
#

# 3. Register a data callback function that returns your data on demand. It
#    has to return an instance of Data(), which accepts any of the following:
#       - `list`
#       - `numpy.ndarray`
#       - `xarray.DataArray`
@fit.callback_data
def get_data(label):
    if label == 'data1':
        return Data(x=[1, 2, 3], y=[4, 10, -3])
    elif label == 'data1':
        return Data(x=[1, 2, 3], y=[-1, -2, -3])

# 4. Register a fit callback function that is used to fit the data. It is
#    passed directly to scipy.optimize.curve_fit().
#    Note: It may be beneficial to also specify @fit.callback_guess (see below)
@fit.set_fitfunc
def func(x, A, B):
    return A*x + B

```

Additionally, the app offeres a few more callbacks, which are optional:
```python
# (Optional) Provide a longer description for the datasets. Return `str`.
@fit.callback_metadata
def get_guess(label):
    return {
        'data1': 'Dataset 1, monday, weather=sunny',
        'data2': 'Dataset 2, friday, weather=raining',
    }[label]

# (Optional) Provide default initial values for the fit parameters.
#            Return `list`, `numpy.ndarray`, `xarray.DataArray`.
@fit.callback_guess
def get_guess(label):
    #       A  B
    return [1, 0]
```

The current fit results are contained in a dict object:
```python
>>> fit.fit_results
{'args': array([-3011.91991276,   943.59548712]),
 'argsErr': array([361.71457033,  86.88364269]),
 'params': array(['A', 'B'], dtype='<U1'),
 'label': (20631, 11),
 'guess': array([1, 1]),
 'data': Data(x, y, yerr),
 'selected': array([22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35])}
```

The app starts running in a background thread the moment you run `get_fitapp()`
and keeps running until you end the script or close the jupyter notebook.
To create more than one app, specify different `port` for each of them (pick an
arbitrary 4-digit number). When the app is running, feel free to change
the `get_data` callback and `fitfunc` any time by re-applying the appropriate
decorators to the new functions and refreshing the browser window.

### Mouse & keyboard control of the app

- `MouseWheel` - zoom in, zoom out
- `Ctrl + LeftMouse` - drag the mouse cursor to zoom in on the selected area
- `Shift + LeftMouse` - drag the mouse cursor to select points to fit
- `Ctrl + Shift + LeftMouse` - drag the mouse cursor to unselect points to fit
- Toggle on the "Fit data" switch in the panel on the right to see the fitted curve

## Development

Install the dependencies

```bash
cd svelte-app

npm install

python -m venv venv  # Requires python 3.7+
pip install -r requirements.txt
```

Then start [Rollup](https://rollupjs.org) (automatically compiles the svelte
app when code is changed)

```bash
npm run dev
```

and the flask server

```bash
python
```

and navigate to [127.0.0.1:5050](http://127.0.0.1:5050).

To create an optimized version of the app use

```bash
npm run build
```
