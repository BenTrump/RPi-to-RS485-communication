
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1,
                      bytesize=8, parity="N", baudrate=9600, timeout=0.3)

connection = client.connect()
print(connection)

read_coils = client.read_coils(1, 4, unit=0x01)
read_input_status = client.read_discrete_inputs(1, 4, unit=0x01)
read_holding_reg = client.read_holding_registers(1, 4, unit=0x01)
read_input_reg = client.read_input_registers(6, 4, unit=0x01)  # Start register, num of registers to read, slave ID
print("From input registers: " + read_input_reg.registers)
print("From coils: " + read_coils.registers)
print("From input status: " + read_input_status.registers)
print("From holding registers: " + read_holding_reg.registers)

