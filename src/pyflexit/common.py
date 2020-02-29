import math
import struct
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Tuple

from pyflexit.utils import registers_to_values, value_to_registers


class Regtype(Enum):
    INPUT = 0
    HOLDING = 1


@dataclass
class Register:
    regtype: Regtype
    addr: int
    data_type: str
    post_read: Callable = lambda x: x
    pre_write: Callable = lambda x: x

    @property
    def count(self) -> int:
        return math.ceil(struct.calcsize(self.data_type) / 2)


class CommonAPI:
    """This is a base class to be inherited by the different Flexit model
    classes. This ensures compatibility across different Flexit models.
    """

    class VentMode(Enum):
        # Each subclass must define their own ventilation modes
        pass

    def __init__(self, client, unit: int):
        self._client = client
        self._unit = unit
        self._REGISTERS: Dict[str, Register] = dict()

    @property
    def outside_air_temp(self) -> float:
        return self._get_register_value("OutsideAirTemp")

    @property
    def extract_air_temp(self) -> float:
        return self._get_register_value("ExtractAirTemp")

    @property
    def supply_air_temp(self) -> float:
        return self._get_register_value("SupplyAirTemp")

    @property
    def air_temp_setpoint(self) -> float:
        """Get the temperature setpoint for supply air"""
        return self._get_register_value("SetpointSupplyAirTemp")

    @air_temp_setpoint.setter
    def air_temp_setpoint(self, temperature) -> None:
        """Set the temperature setpoint for supply air"""
        self._write_register_value("SetpointSupplyAirTemp", temperature)

    @property
    def vent_modes(self) -> Tuple[str, ...]:
        """Returns a tuple of strings with all the valid ventilation modes"""
        return tuple(self.VentMode.__members__.keys())

    @property
    def vent_mode(self) -> str:
        """Return a string with the current fan mode."""
        register_value = self._get_register_value("SetVentMode")
        return self.VentMode(register_value).name

    @vent_mode.setter
    def vent_mode(self, vent_mode: str) -> None:
        """Set new ventilation mode.
        The input string must be one the values returned by self.fan_modes

        Args:
            vent_mode (str): The ventilation mode to change to
        """
        if vent_mode not in self.VentMode.__members__:
            raise ValueError(f"Illegal ventilation mode: {vent_mode}. "
                             f"Supported values: {self.vent_modes}")
        value = self.VentMode.__members__[vent_mode].value
        self._write_register_value("SetVentMode", value)

    @property
    def heat_exchanger_speed(self) -> float:
        return self._get_register_value("HeatExchangerSpeed")

    @property
    def electric_heater_power(self) -> float:
        return self._get_register_value("ElectricAirHeaterPower")

    @property
    def filter_runtime(self) -> float:
        return self._get_register_value("FilterRunTime")

    def _get_register_value(self, register_name: str):
        """Get value from modbus register(s)"""
        if register_name not in self._REGISTERS.keys():
            raise ValueError(f"Unknown register name: {register_name}")
        register = self._REGISTERS[register_name]
        modbus_read_func = {
            Regtype.INPUT: self._client.read_input_registers,
            Regtype.HOLDING: self._client.read_holding_registers
        }
        response = modbus_read_func[register.regtype](
            unit=self._unit,
            address=register.addr,
            count=register.count)
        if response.isError():
            warnings.warn(f"Value not defined")
            return None
        value = registers_to_values(response.registers, register.data_type)[0]
        return register.post_read(value)

    def _write_register_value(self, register_name: str, value) -> None:
        """Write value to modbus register(s)"""
        if register_name not in self._REGISTERS.keys():
            raise ValueError(f"Unknown register name: {register_name}")
        register = self._REGISTERS[register_name]
        value = register.pre_write(value)
        data = value_to_registers(value, register.data_type)
        self._client.write_registers(unit=self._unit,
                                     address=register.addr,
                                     values=data)
