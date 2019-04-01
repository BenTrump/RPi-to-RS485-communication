
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
# from pymodbus.register_read_message import ReadInputRegistersResponse
import tkinter as tk
from threading import Timer


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

        self.lbl_slave_id = tk.Label(self, text="Slave ID: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_slave_id.grid(row=1, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_data_entry = tk.Label(self, text="Output data: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_data_entry.grid(row=2, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_data_return = tk.Label(self, text="Return data: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_data_return.grid(row=3, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_comms_status = tk.Label(self, text="Status: ", font="Arial 12 bold", anchor=tk.E, width=15)
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
        try:
            data = self.txt_data_entry.get().split()
            fixed_data = list(map(int, data))
            print("Sending: " + "-".join(data))
            self.gui.client.write_registers(values=fixed_data, address=40001, unit=0x01)
            self.display_status.config(bg="green")
            timer = Timer(2.0, self.normal_status)
            timer.start()
        except IOError:
            self.display_status.config(bg="red")
            timer = Timer(2.0, self.normal_status)
            timer.start()
            # Todo: find the actual error
            # Todo: make the display status a better color
            # Todo: put timer outside of try except, doesn't need to be in both

    def write_to_single_reg(self):
        try:
            data = self.txt_data_entry.get().split()
            print("Sending: " + "-".join(data[0]))
            self.gui.client.write_register(value=data[0], address=40001, unit=0x01)
        except IOError:
            self.display_status.config(bg="red")
            timer = Timer(2.0, self.normal_status)
            timer.start()
            # Todo: find the actual error

    def read_holding_reg(self):
        try:
            register_data = self.gui.client.read_holding_registers(40001, 4, unit=0x01)
            self.txt_data_return.config(text=register_data.registers)
            print("Data from registers: ", end="")
            print(register_data.registers)
            self.txt_data_entry.config(text=" ")
        except IOError:
            self.display_status.config(bg="red")
            timer = Timer(2.0, self.normal_status)
            timer.start()
            # Todo: find the actual error

    def normal_status(self):
        self.display_status.config(bg="sky blue")


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
