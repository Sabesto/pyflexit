from enum import Enum

from pyflexit.common import CommonAPI, Register, Regtype

REGISTERS = {
    "OutsideAirTemp": Register(Regtype.INPUT, 1, "f"),
    "SupplyAirTemp": Register(Regtype.INPUT, 5, "f"),
    "ExtractAirTemp": Register(Regtype.INPUT, 9, "f"),
    "ExhaustAirTemp": Register(Regtype.INPUT, 13, "f"),
    "SetpointAwaySupplyAirTemp": Register(Regtype.HOLDING, 1163, "f"),
    "SetpointHomeSupplyAirTemp": Register(Regtype.HOLDING, 1155, "f"),

    "HeatExchangerSpeed": Register(Regtype.HOLDING, 1, "f"),
    "ElectricAirHeaterPower": Register(Regtype.HOLDING, 13, "f"),

    "VentMode": Register(Regtype.INPUT, 3034, "H"),
    "SetVentMode": Register(Regtype.HOLDING, 2013, "H"),
    "ExhaustFanSpeed": Register(Regtype.HOLDING, 9, "f"),
    "SupplyFanSpeed": Register(Regtype.HOLDING, 5, "f"),

    "FilterRunTime": Register(Regtype.HOLDING, 1271, "f"),
    "FilterRemainingTime": Register(Regtype.HOLDING, 1269, "f"),

    "RoomHumidity1": Register(Regtype.INPUT, 1001, "f"),
    "RoomHumidity2": Register(Regtype.INPUT, 1003, "f"),
    "RoomHumidity3": Register(Regtype.INPUT, 1005, "f"),
    "RoomAirQuality": Register(Regtype.INPUT, 1007, "f"),
}


class Nordic(CommonAPI):
    """This class supports the Flexit Nordic models (S2, S3, S4, CL2,
    CL3 and CL4). The climate centrals EcoNordic W4 and WH4 are also
    supported, but (currently) only the ventilation part.

    Example:
        This is an example for a Flexit Nordic aggregate::

            import pyflexit
            from pymodbus.client.sync import ModbusSerialClient

            client = ModbusSerialClient(
                method='rtu',
                port='/dev/ttyUSB0',
                stopbits=1,
                bytesize=8,
                parity='E',
                baudrate=9600,
                timeout=2)
            client.connect()
            nordic_unit = pyflexit.aggregate(client, unit=1, model="Nordic"))
    """

    class VentMode(Enum):
        """For the Nordic series, these ventilation modes are supported"""
        Off = 1
        Away = 2
        Home = 3
        High = 4

    def __init__(self, client, unit: int):
        super().__init__(client, unit)
        self._REGISTERS = REGISTERS

    @property
    def air_temp_setpoint(self):
        """Get or set the temperature setpoint for supply air.

        The Nordic series have two separate target temperatures, one for
        "Home" and one for "Away". If the current operating mode is "Away",
        the Away-setpoint is returned. Otherwise, the Home-setpoint is
        returned.

        Example:
            >>> unit.air_temp_setpoint = 21
            >>> unit.air_temp_setpoint
            21.0
        """
        if self.vent_mode == self.VentMode.Away.name:
            return self.away_temp_setpoint
        else:
            return self.home_temp_setpoint

    @air_temp_setpoint.setter
    def air_temp_setpoint(self, temperature: float) -> None:
        """Set the temperature setpoint for supply air.

        The Nordic series have two separate target temperatures, one for
        "Home" and one for "Away". If the current operating mode is "Away",
        the Away-setpoint is changed. Otherwise, the Home-setpoint is
        changed.
        """
        if self.vent_mode == self.VentMode.Away.name:
            self.away_temp_setpoint = temperature
        else:
            self.home_temp_setpoint = temperature

    @property
    def home_temp_setpoint(self) -> float:
        """Get or set the target temperature for supply air when in
        Home-mode.

        In addition to the ``air_temp_setpoint`` property which depends on
        the current ventilation mode, it is also possible to get or set the
        "Home"-setpoint directly, using this property.

        Example:
            >>> nordic_unit.away_temp_setpoint = 23
            >>> nordic_unit.away_temp_setpoint
            23.0
        """
        return self._get_register_value("SetpointHomeSupplyAirTemp")

    @home_temp_setpoint.setter
    def home_temp_setpoint(self, value: float) -> None:
        self._write_register_value("SetpointHomeSupplyAirTemp", value)

    @property
    def away_temp_setpoint(self) -> float:
        """Get or set the target temperature for supply air when in
        Away-mode.

        In addition to the ``air_temp_setpoint`` property which depends on
        the current ventilation mode, it is also possible to get or set the
        "Away"-setpoint directly, using this property.

        Example:
            >>> nordic_unit.away_temp_setpoint = 19
            >>> nordic_unit.away_temp_setpoint
            19.0
        """
        return self._get_register_value("SetpointAwaySupplyAirTemp")

    @away_temp_setpoint.setter
    def away_temp_setpoint(self, value: float) -> None:
        self._write_register_value("SetpointAwaySupplyAirTemp", value)

    @property
    def exhaust_air_temp(self) -> float:
        """Get exhaust air temperature. This is the temperature being blown
        out of the house.
        """
        return self._get_register_value("ExhaustAirTemp")

    @property
    def exhaust_fan_speed(self) -> float:
        """Get speed of the exhaust air fan, in percent from 0-100."""
        return self._get_register_value("ExhaustFanSpeed")

    @property
    def supply_fan_speed(self) -> float:
        """Get speed of supply air fan, in percent from 0-100."""
        return self._get_register_value("SupplyFanSpeed")

    @property
    def filter_remaining_time(self) -> int:
        """Time until filter change (hours)."""
        return self._get_register_value("FilterRemainingTime")

    @property
    def room_humidity_1(self) -> float:
        """Get value of humidity sensor 1, in percent from 0-100.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity1")

    @property
    def room_humidity_2(self) -> float:
        """Get value of humidity sensor 1, in percent from 0-100.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity2")

    @property
    def room_humidity_3(self) -> float:
        """Get value of humidity sensor 1, in percent from 0-100.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity3")

    @property
    def room_airquality(self) -> float:
        """Get value of air quality sensor 1, in ppm from 0-2000.

        This is only available if you have a CI75 adapter and a CI76 sensor.
        """
        return self._get_register_value("RoomAirQuality")

    @property
    def efficiency(self) -> float:
        """Calculate the efficiency of the heat exchanger. The
        efficiency for a counterflow heat exchanger is defined by

        .. math::
            \\eta = \\frac{T_{hot,in} - T_{hot,out}}{T_{hot,in} - T_{cold,in}}

        and will be a number between 0 and 1.

        Example:
            >>> print(f"Efficiency: {100 * nordic_unit.efficiency:2.1f}%")
            Efficiency: 76.9%
        """
        eta = (self.extract_air_temp - self.exhaust_air_temp) / \
              (self.extract_air_temp - self.outside_air_temp)
        return eta
