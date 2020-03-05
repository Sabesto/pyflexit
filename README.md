# Python Library for Flexit ventilation aggregates

Supported modbus interfaces:
* Flexit K2, UNI 2, UNI 3 and UNI 4: Via the CI66 modbus adapter
* Nordic S2, S3, S4, CL2, CL3, CL4
* EcoNordic W4, WH4

Simple helper library for controlling Flexit A/C units. In order to manage a Flexit CI66 modbus adapter, you would say:

```python
import pyflexit
from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    stopbits=1,
    bytesize=8,
    parity='E',
    baudrate=56000,
    timeout=2)
client.connect()
unit = pyflexit.aggregate(client, unit=21, model="CI66"))
```

And then you could do things like:
```python
>>> unit.air_temp_setpoint = 21
>>> unit.air_temp_setpoint
21.0
```

# Development
If you want to help with development or run your own development version locally:

## Get a recent Python version
You will need Python 3.7.x or newer. You can possibly use [pyenv](https://github.com/pyenv/pyenv) to install / manage multiple versions of Python (see [pyenv-installer](https://github.com/pyenv/pyenv-installer) for an easy install, or [pyenv-win](https://github.com/pyenv-win/pyenv-win) project if you're on Windows).

## Install poetry
Install [Poetry](https://python-poetry.org/docs/#installation), and possibly change the default configuration such that virtual environments are created inside your project:
```bash
poetry config virtualenvs.in-project true
```

## Install development version
Start by cloning this repository to a local directory. Then use poetry to install a development version of pyflexit inside a virtual environment. From inside the project directory, run:
```bash
poetry install
```

In order to activate the newly created environment and enable you to run the code, you could say:
```bash
poetry shell
```

PS: This project doesn't automatically install pymodbus, so you need to [install that manually](https://pymodbus.readthedocs.io/en/latest/readme.html#installing) if you want to talk to a Flexit aggregate.


## Run all tests
If you make any changes to the code, it is important to check that all the tests are still OK. In order to run the tests inside your virtual environment, run:
```bash
poetry run pytest tests src
```

In order to test everything under both Python 3.7 and 3.8 (this requires you to have both versions available, e.g. via pyenv), run:
```bash
poetry run tox
⋮
⋮
  py37: commands succeeded
  py38: commands succeeded
  lint: commands succeeded
  docs: commands succeeded
  congratulations :)
```

## Build and release new package
1) Update version number in `pyproject.toml`
1) Commit and push change
1) Create new release tag in git/GitHub
1) Build new package and update to pypi:
```bash
poetry build
poetry publish
```
