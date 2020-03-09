import pytest

import pyflexit
from pyflexit.common import Regtype


def test_init_manual():
    unit = pyflexit.aggregate("dummy", 21, model="CI66")
    assert isinstance(unit, pyflexit.CI66)

    unit = pyflexit.aggregate("dummy", 1, model="Nordic")
    assert isinstance(unit, pyflexit.Nordic)

    with pytest.raises(ValueError):
        pyflexit.aggregate("dummy", 1, model="Illegal")


def test_init_autodetect(modbus_client):

    modbus_client.REGISTERS[(Regtype.HOLDING, 9070)] = None
    unit = pyflexit.aggregate(modbus_client, unit=1)
    assert isinstance(unit, pyflexit.CI66)

    # UTF-8: /4
    modbus_client.REGISTERS[(Regtype.HOLDING, 9070)] = [0]*9 + [12084]
    unit = pyflexit.aggregate(modbus_client, unit=1)
    assert isinstance(unit, pyflexit.Nordic)

    # UTF-8: /5
    modbus_client.REGISTERS[(Regtype.HOLDING, 9070)] = [0]*9 + [12085]
    unit = pyflexit.aggregate(modbus_client, unit=1)
    assert isinstance(unit, pyflexit.Nordic)

    with pytest.raises(ValueError):
        modbus_client.REGISTERS[(Regtype.HOLDING, 9070)] = [0] * 10
        pyflexit.aggregate(modbus_client, unit=1)
