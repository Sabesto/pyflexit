import pytest

from pyflexit import common


def test_value_to_registers():
    regs = common.value_to_registers(-1.2, "f")
    assert regs == (49049, 39322)

    regs = common.value_to_registers(10, "h")
    assert regs == (10,)


def test_registers_to_value():
    regs = (49049, 39322)
    value = common.registers_to_values(regs, "f")[0]
    assert value == pytest.approx(-1.2)

    regs = [17562, 20480, 1, 2, 1, 17833, 47104]
    values = common.registers_to_values(regs, "fi?f")
    assert values == (1234.5, 65538, True, 5431.0)
