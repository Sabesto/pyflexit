from enum import Enum

from pyflexit.common import CommonAPI, Register, Regtype

REGISTERS = {
    "OutsideAirTemp": Register(
        Regtype.INPUT,
        12,
        "h",
        pre_write=lambda x: int(x * 10),
        post_read=lambda x: x / 10,
    ),
    "SupplyAirTemp": Register(
        Regtype.INPUT,
        10,
        "h",
        pre_write=lambda x: int(x * 10),
        post_read=lambda x: x / 10,
    ),
    "ExtractAirTemp": Register(
        Regtype.INPUT,
        11,
        "h",
        pre_write=lambda x: int(x * 10),
        post_read=lambda x: x / 10,
    ),
    "SetpointSupplyAirTemp": Register(
        Regtype.HOLDING,
        9,
        "h",
        pre_write=lambda x: int(x * 10),
        post_read=lambda x: x / 10,
    ),
    "HeatExchangerSpeed": Register(Regtype.INPUT, 15, "h"),
    "ElectricAirHeaterPower": Register(Regtype.INPUT, 16, "h"),
    "SetVentMode": Register(Regtype.HOLDING, 18, "h"),
    "FilterRunTime": Register(Regtype.INPUT, 9, "H"),
    "HeatingEnabled": Register(Regtype.INPUT, 29, "?"),
    "ReplaceFilterAlarm": Register(Regtype.INPUT, 28, "?"),
}


class CI66(CommonAPI):
    """This class supports the Flexit CI66 modbus adapter, which is
    compatible with the K2, UNI 2, UNI 3 and UNI 4 aggregates.

    Example:
        This is an example for a Flexit CI66 adapter::

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
            ci66_unit = pyflexit.aggregate(client, unit=21, model="CI66")
    """

    class VentMode(Enum):
        Off = 0
        Min = 1
        Normal = 2
        Max = 3

    def __init__(self, client, unit: int):
        super().__init__(client, unit)
        self._REGISTERS = REGISTERS

    @property
    def heating_enabled(self) -> bool:
        """Is the heating module enabled?

        Returns:
            ``True`` or ``False`` depending on the status.
        """
        return self._get_register_value("HeatingEnabled")

    @property
    def replace_filter_alarm(self) -> bool:
        """
        Status of filter change alarm

        Returns:
            ``True`` when it's time to change the filter, otherwise ``False``.
        """
        return self._get_register_value("ReplaceFilterAlarm")
