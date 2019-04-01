
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
# from pymodbus.register_read_message import ReadInputRegistersResponse
import tkinter as tk


class Main(tk.Frame):
    def __init__(self, gui, *args, **kwargs):
        tk.Frame.__init__(self, master=gui.master, *args, **kwargs)
        self.grid(row=0, column=0)
        self.gui = gui

        self.btn_write_multi_regs = tk.Button(self, text="Write to multiple registers", height=2, width=30)
        self.btn_write_multi_regs.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_write_multi_regs.config(font="Arial 12 bold", command=self.write_to_multi_regs)
        self.btn_write_single_reg = tk.Button(self, text="Write to single register", height=2, width=30)
        self.btn_write_single_reg.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_write_single_reg.config(font="Arial 12 bold")
        self.btn_read_regs = tk.Button(self, text="Read holding registers", height=2, width=30)
        self.btn_read_regs.grid(row=3, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_read_regs.config(font="Arial 12 bold", command=self.read_holding_reg)

        self.lbl_slave_id = tk.Label(self, text="Slave ID: ", font="Arial 12 bold", anchor=tk.E, width=10)
        self.lbl_slave_id.grid(row=1, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_data_entry = tk.Label(self, text="Output data: ", font="Arial 12 bold", anchor=tk.E, width=10)
        self.lbl_data_entry.grid(row=2, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_data_return = tk.Label(self, text="Return data: ", font="Arial 12 bold", anchor=tk.E, width=10)
        self.lbl_data_return.grid(row=3, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_comms_status = tk.Label(self, text="Status: ", font="Arial 12 bold", anchor=tk.E, width=10)
        self.lbl_comms_status.grid(row=4, column=3, padx=(10, 0), pady=(10, 0))

        self.txt_slave_id = tk.Entry(self, font="Arial 12 bold", relief="sunken", width=30)
        self.txt_slave_id.grid(row=1, column=4, padx=(10,  0), pady=(10, 0))
        self.txt_data_entry = tk.Entry(self, font="Arial 12 bold", relief="sunken", width=30)
        self.txt_data_entry.grid(row=2, column=4, padx=(10, 0), pady=(10, 0))
        self.txt_data_return = tk.Label(self, font="Arial 12 bold", relief="sunken", width=27, bg="white", bd=1)
        self.txt_data_return.grid(row=3, column=4, padx=(10, 0), pady=(10, 0))

        self.display_status = tk.Label(self, relief="raised", width=20, height=2, bg="sky blue")
        self.display_status.grid(row=4, column=4, padx=(10, 0), pady=(10, 0), sticky=tk.W)

    def write_to_multi_regs(self):
        data = self.txt_data_entry.get()
        print("Sending: " + data)
        self.gui.client.write_registers(value=[5, 6, 7], address=1, unit=0x01)

    def write_to_single_reg(self):
        data = self.txt_data_entry.get()
        print("Sending: " + data)
        self.gui.client.write_register(value=15, address=1, unit=0x01)

    def read_holding_reg(self):
        register_data = self.gui.client.read_holding_registers(1, 4, unit=0x01)
        print("Data from registers: " + register_data.registers)


class GUI(object):
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("RS485 Communication Tester")
        self.master.geometry("800x400")
        self.main = Main(self)

        self.client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1,
                                   bytesize=8, parity="N", baudrate=9600, timeout=0.3)
        connection = self.client.connect()
        print(connection)

        self.master.mainloop()


test = GUI()
