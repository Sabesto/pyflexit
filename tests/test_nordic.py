import pytest

import pyflexit
from pyflexit.common import Regtype


def test_nordic(modbus_client, common_api):
    unit = pyflexit.Nordic(modbus_client, 1)
    common_api(modbus_client, unit)

    assert unit.vent_modes == ("Off", "Away", "Home", "High")

    unit.vent_mode = "Home"
    assert unit.vent_mode == "Home"

    modbus_client.inject_value(unit._REGISTERS["ExhaustAirTemp"], 0.1)
    assert unit.exhaust_air_temp == pytest.approx(0.1)

    unit.vent_mode = "Home"
    unit.air_temp_setpoint = 21.5
    assert unit.air_temp_setpoint == pytest.approx(21.5)
    assert unit.home_temp_setpoint == pytest.approx(21.5)

    unit.vent_mode = "Away"
    unit.air_temp_setpoint = 19.0
    assert unit.air_temp_setpoint == pytest.approx(19.0)
    assert unit.away_temp_setpoint == pytest.approx(19.0)

    modbus_client.inject_value(unit._REGISTERS["ExhaustFanSpeed"], 65.0)
    assert unit.exhaust_fan_speed == pytest.approx(65.0)

    modbus_client.inject_value(unit._REGISTERS["SupplyFanSpeed"], 62.0)
    assert unit.supply_fan_speed == pytest.approx(62.0)

    modbus_client.inject_value(unit._REGISTERS["FilterRemainingTime"], 2016)
    assert unit.filter_remaining_time == 2016

    modbus_client.inject_value(unit._REGISTERS["RoomHumidity1"], 31.2)
    assert unit.room_humidity_1 == pytest.approx(31.2)

    modbus_client.inject_value(unit._REGISTERS["RoomHumidity2"], 41.2)
    assert unit.room_humidity_2 == pytest.approx(41.2)

    modbus_client.inject_value(unit._REGISTERS["RoomHumidity3"], 51.2)
    assert unit.room_humidity_3 == pytest.approx(51.2)

    modbus_client.inject_value(unit._REGISTERS["RoomAirQuality"], 500)
    assert unit.room_airquality == pytest.approx(500)

    modbus_client.REGISTERS[(Regtype.HOLDING, 13)] = None
    with pytest.warns(UserWarning):
        assert unit.electric_heater_power == 0
