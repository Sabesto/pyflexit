from typing import List

import pytest

from pyflexit.common import Register, Regtype
from pyflexit.utils import value_to_registers


class ModbusResponse:
    def __init__(self, registers: List[int], error=False):
        self.registers = registers
        self.error = error

    def isError(self):
        return self.error


@pytest.fixture
def modbus_client():
    class ModbusClient:
        """A fake modbus client that can store and retrieve data"""

        def __init__(self):
            self.REGISTERS = dict()

        def inject_value(self, register: Register, value):
            """Store a value in a register, using specified data type"""
            key = (register.regtype, register.addr)
            value = register.pre_write(value)
            self.REGISTERS[key] = value_to_registers(value, register.data_type)

        def _read_register(self, key):
            """Get register values from the internal register storage"""
            registers = self.REGISTERS[key]
            return ModbusResponse(registers)

        def read_input_registers(self, unit, address, count) -> ModbusResponse:
            """Emulate the function from pymodbus.client"""
            if address == 0:
                return ModbusResponse([], error=True)
            return self._read_register((Regtype.INPUT, address))

        def read_holding_registers(self, unit, address, count) -> \
                ModbusResponse:
            """Emulate the function from pymodbus.client"""
            return self._read_register((Regtype.HOLDING, address))

        def write_registers(self, unit, address, values):
            """Emulate the function from pymodbus.client"""
            self.REGISTERS[(Regtype.HOLDING, address)] = values

    return ModbusClient()


@pytest.fixture
def common_api():
    """A fixture that returns the function below. This allows us to run this
    function for each of the Flexit models."""
    return _common_api


def _common_api(modbus_client, unit):
    """All Flexit units that support the Home Assistant API must
    successfully run these tests"""

    modbus_client.inject_value(unit._REGISTERS["OutsideAirTemp"], -5.2)
    assert unit.outside_air_temp == pytest.approx(-5.2)

    modbus_client.inject_value(unit._REGISTERS["ExtractAirTemp"], 22.5)
    assert unit.extract_air_temp == pytest.approx(22.5)

    modbus_client.inject_value(unit._REGISTERS["SupplyAirTemp"], 21.1)
    assert unit.supply_air_temp == pytest.approx(21.1)

    with pytest.raises(ValueError):
        unit.vent_mode = "Illegal"

    modbus_client.inject_value(unit._REGISTERS["HeatExchangerSpeed"], 100)
    assert unit.heat_exchanger_speed == 100

    modbus_client.inject_value(unit._REGISTERS["ElectricAirHeaterPower"], 35)
    assert unit.electric_heater_power == pytest.approx(35)

    modbus_client.inject_value(unit._REGISTERS["FilterRunTime"], 2016)
    assert unit.filter_runtime == 2016

    with pytest.raises(ValueError):
        unit._get_register_value("Illegal")

    with pytest.raises(ValueError):
        unit._write_register_value("Illegal", 0)

    unit._REGISTERS["IllegalAddress"] = Register(Regtype.INPUT, 0, "f")
    with pytest.warns(UserWarning):
        value = unit._get_register_value("IllegalAddress")
    assert value is None