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
    classes. This ensures compatibility across different Flexit models. You
    will not be using this class directly, it is inherited by the CI66 and
    Nordic classes.
    """

    class VentMode(Enum):
        """Each subclass must define their own ventilation modes with the
        proper names and values"""
        pass

    def __init__(self, client, unit: int):
        """Initialize the object.

        Args:
            client: A configured and connected modbus client, as returned by
                ``pymodbus.client.sync.ModbusSerialClient()``
            unit: The modbus ID of your aggregate. For the Nordic series,
                this number would be 1. For CI66, it is configurable with
                dip-switches, but it is typically 21.
        """
        self._client = client
        self._unit = unit
        self._REGISTERS: Dict[str, Register] = dict()

    @property
    def outside_air_temp(self) -> float:
        """Get the measured outside air temperature

        Example:
            >>> unit.outside_air_temp
            -1.2
        """
        return self._get_register_value("OutsideAirTemp")

    @property
    def extract_air_temp(self) -> float:
        """Get the measured air temperature of the air being extracted from
        the rooms. This corresponds to the average temperature in the house.

        Example:
            >>> unit.extract_air_temp
            21.3
        """
        return self._get_register_value("ExtractAirTemp")

    @property
    def supply_air_temp(self) -> float:
        """Get the measured temperature of the supply air. This is the fresh
        air that goes into the rooms.

        Example:
            >>> unit.supply_air_temp
            20.4
        """
        return self._get_register_value("SupplyAirTemp")

    @property
    def air_temp_setpoint(self) -> float:
        """Temperature setpoint for supply air, the property can be read from
        and written to.

        Example:
            >>> unit.air_temp_setpoint = 21
            >>> unit.air_temp_setpoint
            21.0
        """
        return self._get_register_value("SetpointSupplyAirTemp")

    @air_temp_setpoint.setter
    def air_temp_setpoint(self, temperature) -> None:
        """Set the temperature setpoint for supply air"""
        self._write_register_value("SetpointSupplyAirTemp", temperature)

    @property
    def vent_modes(self) -> Tuple[str, ...]:
        """Returns a tuple of strings with all the valid ventilation modes.

        Examples:
            For a CI66 adapter, this would be:

            >>> ci66_unit.vent_modes
            ('Off', 'Min', 'Normal', 'Max')

            For a Nordic series aggregate, this would be:

            >>> nordic_unit.vent_modes
            ('Off', 'Away', 'Home', 'High')
        """
        return tuple(self.VentMode.__members__.keys())

    @property
    def vent_mode(self) -> str:
        """This property can be used to set or get the ventilation
        mode. Whet getting the current ventilation mode, a string is
        returned. When setting the ventilation mode, a string is
        expected. The string needs to be one of the values returned by
        the vent_modes property.

        Examples:
            >>> ci66_unit.vent_mode = "Min"
            >>> ci66_unit.vent_mode
            'Min'

            >>> nordic_unit.vent_mode = "High"
            >>> nordic_unit.vent_mode
            'High'
        """
        register_value = self._get_register_value("SetVentMode")
        return self.VentMode(register_value).name

    @vent_mode.setter
    def vent_mode(self, vent_mode: str) -> None:
        """Set new ventilation mode.
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
        """Gets the current speed of the rotating heat exchanger, in percent
        from 0-100.

        Example:
            >>> unit.heat_exchanger_speed
            100
        """
        return self._get_register_value("HeatExchangerSpeed")

    @property
    def electric_heater_power(self) -> float:
        """Gets the current power of the electric heating coil for supply
        air. In percent from 0-100.

        Example:
            >>> unit.electric_heater_power
            42
        """
        value = self._get_register_value("ElectricAirHeaterPower")
        if value is None:
            # If the heater in the Nordic series is switched off,
            # this register doesn't exists.
            return 0
        return value

    @property
    def filter_runtime(self) -> float:
        """Gets the number of hours in operation since last filter change.

        Example:
            >>> unit.filter_runtime
            1344
        """
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
