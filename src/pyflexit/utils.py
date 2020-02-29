import struct
from typing import Iterable, List


def zero_pad(data_format: str) -> str:
    """Data formats smaller than 16 bits must be zero-padded

    Args:
        data_format (str): A single data format character, see struct module

    Returns:
        A possible zero-padded data format string

    Examples:
        A float doesn't need zero-padding
        >>> zero_pad("f")
        'f'

        A boolean is only one byte, and must be zero-padded
        >>> zero_pad("?")
        'x?'
    """
    if struct.calcsize(data_format) < 2:
        return f"x{data_format}"
    return data_format


def registers_to_values(registers: Iterable[int], data_types: str):
    """Decode a list of registers to value(s), given the specified data type(s).

    The registers argument will typically be the .registers attribute of a
    pymodbus response object.

    Args:
        registers (List[int]): List of register values
        data_types (str): See the struct module for examples

    Returns:
        A tuple with the decoded value(s)

    Examples:
        Decoding a 32-bit float from two registers:
        >>> registers_to_values((17562, 20480), 'f')
        (1234.5,)

        Decoding multiple values of different type from multiple registers:
        >>> registers_to_values([17562, 20480, 1, 2, 1, 17833, 47104], "fi?f")
        (1234.5, 65538, True, 5431.0)
    """
    binary_format = "".join(zero_pad(data_type) for data_type in data_types)
    byte_string = b''.join(struct.pack('>H', r) for r in registers)
    return struct.unpack(f">{binary_format}", byte_string)


def value_to_registers(value, data_type: str) -> List[int]:
    """Encode a value into a list of registers.

    The resulting list of registers can be written to an address:
    write_registers(address, registers, unit=1)

    Args:
        value: The value to be encoded
        data_type (str): The data type, see struct module for examples

    Returns:
        A tuple of registers

    Example:
        Encoding a 32-bit float into two registers:
        >>> value_to_registers(1234.5, 'f')
        [17562, 20480]
    """
    binary_format = zero_pad(data_type)
    bs = struct.pack(f">{binary_format}", value)
    return list(struct.unpack(f">{struct.calcsize(binary_format) // 2}H", bs))
