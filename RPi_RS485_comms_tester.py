
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1,
                      bytesize=8, parity="none", baudrate=9600, timeout=0.3)

connection = client.connect()
print(connection)

value = client.read_input_registers(6, 4, unit=0x01)
print(value.registers)
