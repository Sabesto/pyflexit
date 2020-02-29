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
    """This class supports the Flexit Nordic models (S2, S3, S4, CL3)."""

    class VentMode(Enum):
        Off = 1
        Away = 2
        Home = 3
        High = 4

    def __init__(self, client, unit: int):
        super().__init__(client, unit)
        self._REGISTERS = REGISTERS

    @property
    def air_temp_setpoint(self):
        """Get the temperature setpoint for supply air.

        The Nordic series have two separate target temperatures, one for
        "Home" and one for "Away". If the current operating mode is "Away",
        the Away-setpoint is returned. Otherwise, the Home-setpoint is
        returned."""
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
        """Get target temperature for supply air when in Home-mode"""
        return self._get_register_value("SetpointHomeSupplyAirTemp")

    @home_temp_setpoint.setter
    def home_temp_setpoint(self, value: float) -> None:
        """Set target temperature for supply air when in Home-mode"""
        self._write_register_value("SetpointHomeSupplyAirTemp", value)

    @property
    def away_temp_setpoint(self) -> float:
        """Get target temperature for supply air when in Away-mode"""
        return self._get_register_value("SetpointAwaySupplyAirTemp")

    @away_temp_setpoint.setter
    def away_temp_setpoint(self, value: float) -> None:
        """Set target temperature for supply air when in Away-mode"""
        self._write_register_value("SetpointAwaySupplyAirTemp", value)

    @property
    def exhaust_air_temp(self) -> float:
        """Get exhaust air temperature"""
        return self._get_register_value("ExhaustAirTemp")

    @property
    def exhaust_fan_speed(self) -> float:
        """Get speed of exhaust fan: 0-100%"""
        return self._get_register_value("ExhaustFanSpeed")

    @property
    def supply_fan_speed(self) -> float:
        """Get speed of supply fan: 0-100%"""
        return self._get_register_value("SupplyFanSpeed")

    @property
    def filter_remaining_time(self) -> int:
        """Time until filter change (hours)"""
        return self._get_register_value("FilterRemainingTime")

    @property
    def room_humidity_1(self) -> float:
        """Get value of humidity sensor 1.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity1")

    @property
    def room_humidity_2(self) -> float:
        """Get value of humidity sensor 1.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity2")

    @property
    def room_humidity_3(self) -> float:
        """Get value of humidity sensor 1.

        This is only available if you have a CI75 adapter and a CI77 sensor.
        """
        return self._get_register_value("RoomHumidity3")

    @property
    def room_airquality(self) -> float:
        """Get value of humidity sensor 1.

        This is only available if you have a CI75 adapter and a CI76 sensor.
        """
        return self._get_register_value("RoomAirQuality")
