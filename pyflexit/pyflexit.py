REGMAP_INPUT = {
    'GWYVer':                   {'addr':   0, 'value': 0},
    'CUHWType':                 {'addr':   1, 'value': 0},
    'CUSWRev':                  {'addr':   2, 'value': 0},
    'CPASWRev':                 {'addr':   3, 'value': 0},
    'CPB1SWRev':                {'addr':   4, 'value': 0},
    'CBPS2WRev':                {'addr':   5, 'value': 0},
    'Time1H':                   {'addr':   6, 'value': 0},
    'Time1L':                   {'addr':   7, 'value': 0},
    'FilterTimer':              {'addr':   8, 'value': 0},
    'SupplyAirTemp':            {'addr':   9, 'value': 0},
    'ExtractAirTemp':           {'addr':  10, 'value': 0},
    'OutdoorAirTemp':           {'addr':  11, 'value': 0},
    'ReturnWaterTemp':          {'addr':  12, 'value': 0},
    'Cooling':                  {'addr':  13, 'value': 0},
    'HeatExchanger':            {'addr':  14, 'value': 0},
    'Heating':                  {'addr':  15, 'value': 0},
    'RegulationFanSpeed':       {'addr':  16, 'value': 0},
    'OperTime':                 {'addr':  17, 'value': 0},
    'FilterResetNo':            {'addr':  18, 'value': 0},
    'SupplyAirAlarm':           {'addr':  19, 'value': 0},
    'ExtractAirAlarm':          {'addr':  20, 'value': 0},
    'OutsideAirAlarm':          {'addr':  21, 'value': 0},
    'ReturnWaterAlarm':         {'addr':  22, 'value': 0},
    'FireThermostatAlarm':      {'addr':  23, 'value': 0},
    'FireSmokeAlarm':           {'addr':  24, 'value': 0},
    'FreezeProtectionAlarm':    {'addr':  25, 'value': 0},
    'RotorAlarm':               {'addr':  26, 'value': 0},
    'ReplaceFilterAlarm':       {'addr':  27, 'value': 0},
    'HeatingBatteryActive':     {'addr':  28, 'value': 0},
    'SchActive':                {'addr':  29, 'value': 0},
    'SP0TimeH':                 {'addr':  30, 'value': 0},
    'SP0TimeL':                 {'addr':  31, 'value': 0},
    'SP1TimeH':                 {'addr':  32, 'value': 0},
    'SP1TimeL':                 {'addr':  33, 'value': 0},
    'SP2TimeH':                 {'addr':  34, 'value': 0},
    'SP2TimeL':                 {'addr':  35, 'value': 0},
    'SP3TimeH':                 {'addr':  36, 'value': 0},
    'SP3TimeL':                 {'addr':  37, 'value': 0},
    'VVX1TimeH':                {'addr':  38, 'value': 0},
    'VVX1TimeL':                {'addr':  39, 'value': 0},
    'EV1TimeH':                 {'addr':  40, 'value': 0},
    'EV1TimeL':                 {'addr':  41, 'value': 0},
    'OperTimeH':                {'addr':  42, 'value': 0},
    'OperTimeL':                {'addr':  43, 'value': 0},
    'FilterTimeH':              {'addr':  44, 'value': 0},
    'FilterTimeL':              {'addr':  45, 'value': 0},
    'FilterAlarmPeriod':        {'addr':  46, 'value': 0},
    'ActualSetAirTemperature':  {'addr':  47, 'value': 0},
    'ActualSetAirSpeed':        {'addr':  48, 'value': 0}
}
REGMAP_HOLDING = {
    'SupplyAirSpeed1':          {'addr':  0, 'value': 0},
    'SupplyAirSpeed2':          {'addr':  1, 'value': 0},
    'SupplyAirSpeed3':          {'addr':  2, 'value': 0},
    'SupplyAirSpeed4':          {'addr':  3, 'value': 0},
    'ExtractAirSpeed1':         {'addr':  4, 'value': 0},
    'ExtractAirSpeed2':         {'addr':  5, 'value': 0},
    'ExtractAirSpeed3':         {'addr':  6, 'value': 0},
    'ExtractAirSpeed4':         {'addr':  7, 'value': 0},
    'SetAirTemperature':        {'addr':  8, 'value': 0},
    'SupplyAirMinTemp':         {'addr':  9, 'value': 0},
    'SupplyAirMaxTemp':         {'addr': 10, 'value': 0},
    'CoolingOutdoorAirMinTemp': {'addr': 11, 'value': 0},
    'ForcedVentSpeed':          {'addr': 12, 'value': 0},
    'ForcedVentTime':           {'addr': 13, 'value': 0},
    'AirRegulationType':        {'addr': 14, 'value': 0},
    'CoolingActive':            {'addr': 15, 'value': 0},
    'ForcedVentilation':        {'addr': 16, 'value': 0},
    'SetAirSpeed':              {'addr': 17, 'value': 0},
    'TimeH':                    {'addr': 18, 'value': 0},
    'TimeL':                    {'addr': 19, 'value': 0},
    'Unknown1':                 {'addr': 20, 'value': 0},
    'FireSmokeMode':            {'addr': 21, 'value': 0}
}


class pyflexit(object):
    def __init__(self, conn, slave, update_on_read=False):
        self._conn = conn
        self._input_regs = REGMAP_INPUT
        self._holding_regs = REGMAP_HOLDING
        self._slave = slave
        self._target_temp = None
        self._current_temp = None
        self._current_fan = None
        self._current_operation = None
        self._filter_hours = None
        self._filter_alarm = None
        self._heat_recovery = None
        self._heater_enabled = False
        self._heating = None
        self._cooling = None
        self._alarm = False
        self._update_on_read = update_on_read

    def update(self):
        ret = True
        try:
            result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=0,
                count=len(self._input_regs)).registers
            result_holding = self._conn.read_holding_registers(
                unit=self._slave,
                address=0,
                count=len(self._holding_regs)).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")
        else:
            for k in self._holding_regs:
                self._holding_regs[k]['value'] = \
                    result_holding[self._holding_regs[k]['addr']]
            for k in self._input_regs:
                self._input_regs[k]['value'] = \
                    result_input[self._input_regs[k]['addr']]

        self._target_temp = \
            (self._input_regs['ActualSetAirTemperature']['value'] / 10.0)
        # Temperature directly after heat recovery and heater
        self._current_temp = \
            (self._input_regs['SupplyAirTemp']['value'] / 10.0)
        self._current_fan = \
            (self._input_regs['ActualSetAirSpeed']['value'])
        # Hours since last filter reset
        self._filter_hours = \
            self._input_regs['FilterTimer']['value']
        # Mechanical heat recovery, 0-100%
        self._heat_recovery = \
            self._input_regs['HeatExchanger']['value']
        # Heater active 0-100%
        self._heating = \
            self._input_regs['Heating']['value']
        # Cooling active 0-100%
        self._cooling = \
            self._input_regs['Cooling']['value']
        # Filter alarm 0/1
        self._filter_alarm = \
            bool(self._input_regs['ReplaceFilterAlarm']['value'])
        # Heater enabled or not. Does not mean it's necessarily heating
        self._heater_enabled = \
            bool(self._input_regs['HeatingBatteryActive']['value'])
        # Current operation mode
        if self._heating:
            self._current_operation = 'Heating'
        elif self._cooling:
            self._current_operation = 'Cooling'
        elif self._heat_recovery:
            self._current_operation = 'Recovering'
        elif self._input_regs['ActualSetAirSpeed']['value']:
            self._current_operation = 'Fan Only'
        else:
            self._current_operation = 'Off'

        return ret

    def get_raw_input_register(self, name):
        """Get raw register value by name."""
        if self._update_on_read:
            self.update()
        return self._input_regs[name]

    def get_raw_holding_register(self, name):
        """Get raw register value by name."""
        if self._update_on_read:
            self.update()
        return self._holding_regs[name]

    def set_raw_holding_register(self, name, value):
        """Write to register by name."""
        self._conn.write_register(
            unit=self._slave,
            address=(self._holding_regs[name]['addr']),
            value=value)

    def set_temp(self, temp):
        self._conn.write_register(
            unit=self._slave,
            address=(self._holding_regs['SetAirTemperature']['addr']),
            value=round(temp * 10.0))

    def set_fan_speed(self, fan):
        self._conn.write_register(
            unit=self._slave,
            address=(self._holding_regs['SetAirSpeed']['addr']),
            value=fan)

    @property
    def get_temp(self):
        """Get the current temperature."""
        if self._update_on_read:
            self.update()
        return self._current_temp

    @property
    def get_target_temp(self):
        """Get target temperature."""
        if self._update_on_read:
            self.update()
        return self._target_temp

    @property
    def get_filter_hours(self):
        """Get the number of hours since filter reset."""
        if self._update_on_read:
            self.update()
        return self._filter_hours

    @property
    def get_operation(self):
        """Return the current mode of operation."""
        if self._update_on_read:
            self.update()
        return self._current_operation

    @property
    def get_fan_speed(self):
        """Return the current fan speed (0-4)."""
        if self._update_on_read:
            self.update()
        return self._current_fan

    @property
    def get_heat_recovery(self):
        """Return current heat recovery percentage."""
        if self._update_on_read:
            self.update()
        return self._heat_recovery

    @property
    def get_heating(self):
        """Return heater percentage."""
        if self._update_on_read:
            self.update()
        return self._heating

    @property
    def get_heater_enabled(self):
        """Return heater enabled."""
        if self._update_on_read:
            self.update()
        return self._heater_enabled

    @property
    def get_cooling(self):
        """Cooling active percentage."""
        if self._update_on_read:
            self.update()
        return self._cooling

    @property
    def get_filter_alarm(self):
        """Change filter alarm."""
        if self._update_on_read:
            self.update()
        return self._filter_alarm
