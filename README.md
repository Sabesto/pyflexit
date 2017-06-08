# Python Library for Flexit CI66

Simple helper library for controlling Flexit A/C units


```py
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

unit.set_fan_speed(3)
unit.set_temp(11)

client.close()
```