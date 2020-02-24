from abc import ABC, abstractmethod
from typing import Tuple, List

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder


def registers_to_value(registers: List[int], data_type: str):
    """Decode a list of registers to a value, given the specified data type.

    The registers argument will typically be the .registers attribute of a
    pymodbus response object.

    Args:
        registers (List[int]): List of register values
        data_type (str): See the struct module for examples

    Returns:
        The decoded value
    """
    decoder = BinaryPayloadDecoder.fromRegisters(
        registers, byteorder=Endian.Big)
    if data_type == 'f':
        return decoder.decode_32bit_float()
    if data_type == 'I':
        return decoder.decode_32bit_uint()
    if data_type == 'H':
        return decoder.decode_16bit_int()
    raise ValueError(f"Unknown data type: {data_type}")


def value_to_registers(value, data_type: str) -> List[int]:
    """Encode a value into a list of registers.

    The resulting list of registers can be written to an address:
    write_registers(address, registers, unit=1)

    Args:
        value: The value to be encoded
        data_type (str): The data type, see struct module for examples

    Returns:
        The list of registers
    """
    encoder = BinaryPayloadBuilder(byteorder=Endian.Big)
    if data_type == 'f':
        encoder.add_32bit_float(value)
    elif data_type == 'I':
        encoder.add_32bit_uint(value)
    elif data_type == 'H':
        encoder.add_16bit_int(value)
    else:
        ValueError(f"Unknown data type: {data_type}")
    return encoder.to_registers()


class HomeAssistantAPI(ABC):
    """This is an abstract base class to be inherited by the different Flexit
    model classes. We define an API that will be used by the Home Assistant
    climate component. This ensures Home Assistant compatibility across
    different Flexit models."""

    @property
    @abstractmethod
    def current_temperature(self) -> float:
        """Return current measured temperature (for supply air)"""
        pass

    @abstractmethod
    def set_temperature(self, temperature: float) -> None:
        """Set target temperature (for supply air)"""
        pass

    @property
    @abstractmethod
    def fan_modes(self) -> Tuple[str, ...]:
        """Return a tuple of strings with names of supported fan modes"""
        pass

    @property
    @abstractmethod
    def fan_mode(self) -> str:
        """Return current fan mode as a string"""
        pass

    @abstractmethod
    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new fan mode. Input must be one of self.fan_modes"""
        pass
