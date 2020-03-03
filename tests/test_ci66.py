import pyflexit


def test_ci66(modbus_client, common_api):
    unit = pyflexit.CI66(modbus_client, 21)
    common_api(modbus_client, unit)

    assert unit.vent_modes == ("Off", "Min", "Normal", "Max")

    unit.vent_mode = "Max"
    assert unit.vent_mode == "Max"

    unit.air_temp_setpoint = 21.5
    assert unit.air_temp_setpoint == 21.5

    modbus_client.inject_value(unit._REGISTERS["HeatingEnabled"], True)
    assert unit.heating_enabled is True

    modbus_client.inject_value(unit._REGISTERS["ReplaceFilterAlarm"], True)
    assert unit.replace_filter_alarm is True
