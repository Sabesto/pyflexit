#!/usr/bin/python3
import time
from pyflexit import pyflexit
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu',
                      port='/dev/ttyUSB0',
                      stopbits=1,
                      bytesize=8,
                      parity='E',
                      baudrate=56000,
                      timeout=2)
client.connect()
unit = pyflexit.pyflexit(client, 21)
unit.update()

print("unit.get_temp {}".format(unit.get_temp))
print("unit.get_target_temp {}".format(unit.get_target_temp))
print("unit.get_filter_hours {}".format(unit.get_filter_hours))
print("unit.get_operation {}".format(unit.get_operation))
print("unit.get_fan_speed {}".format(unit.get_fan_speed))
print("unit.get_heat_recovery {}".format(unit.get_heat_recovery))
print("unit.get_heating {}".format(unit.get_heating))
print("unit.get_heater_enabled {}".format(unit.get_heater_enabled))
print("unit.get_cooling {}".format(unit.get_cooling))
print("unit.get_filter_alarm {}".format(unit.get_filter_alarm))


print("Setting fan to 3")
unit.set_fan_speed(3)
time.sleep(3)
unit.update()
print("unit.get_fan_speed {}".format(unit.get_fan_speed))

print("Setting fan to 2")
unit.set_fan_speed(2)
time.sleep(3)
unit.update()
print("unit.get_fan_speed {}".format(unit.get_fan_speed))

print("Setting fan to 3 with set_raw_holding_register()")
unit.set_raw_holding_register('SetAirSpeed', 3)
time.sleep(2)
unit.update()
print("unit.get_fan_speed {}".format(unit.get_fan_speed))

print("Setting fan to 2 with set_raw_holding_register()")
unit.set_raw_holding_register('SetAirSpeed', 2)
time.sleep(2)
unit.update()
print("unit.get_fan_speed {}".format(unit.get_fan_speed))

client.close()
